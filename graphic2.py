from ursina import *
from parsing import Parsing
from ursina.prefabs.first_person_controller import FirstPersonController
from algo_test import BFS


class Graphic:
    def __init__(self, position, all_pos):
        self.app = Ursina(title="fly-in")
        self.generate_world()
        self.player = FirstPersonController(
            z=-0.1,
            origin_y=1,
            speed=20,
            gravity=0,
            y=4
        )
        self.camera = EditorCamera(enabled=False, ignore_paused=True)
        self.camera.y = 5
        self.drones = []
        self.drone_entities = {}   # id -> Entity
        self.all_pos = all_pos
        self.position = position
        self.hub_positions = {
            zone['name']: Vec3(zone['x'] * 2.5, 3, zone['y'] * 2.5)
            for zone in self.all_pos
        }
        # État de chaque drone : id -> {entity, path, seg_idx, progress, speed}
        self.drone_states = {}
        self.hub_positions = {
            zone['name']: Vec3(zone['x'] * 2.5, 3, zone['y'] * 2.5)
            for zone in self.all_pos
        }
        # Capacité de chaque hub
        self.hub_capacity = {
            zone['name']: zone['capacity']
            for zone in self.all_pos
        }

    def generate_world(self):
        self.ground = Entity(
            model="plane",
            collider='box',
            scale=Vec3(110),
            texture='grass',
            texture_scale=(4, 4)
        )
        self.sun = DirectionalLight()
        self.sun.look_at(Vec3(1, -1, -1))
        Sky()

    def run(self):
    # Ursina cherche une fonction globale 'update' dans le scope principal
    # On contourne en créant une Entity dédiée au tick
        updater = Entity()
        updater.update = self._update_drones
        self.app.run()
        
    def generate_map(self):
        for a, b, col_data in self.position:
            if col_data == "purple":    col_data = "violet"
            if col_data == "maroon":    col_data = "brown"
            if col_data in ("darkred", "crimson"): col_data = "brown"
            clean_color = col_data
            if isinstance(col_data, str):
                clean_color = col_data.replace('[color=', '').replace(']', '')
            Entity(
                model='cube',
                origin_y=-0.5,
                scale=Vec3(0.5, 0.5, 0.5),
                texture='brick',
                x=a * 2.5,
                z=b * 2.5,
                collider='box',
                color=getattr(color, clean_color) if hasattr(color, clean_color) else color.white
            )

    def generate_hub_labels(self):
        """Affiche le nom de chaque hub en 3D au-dessus de sa position."""
        for name, pos in self.hub_positions.items():
            Text(
                text=name,
                position=Vec3(pos.x, pos.y + 1.0, pos.z),
                scale=8,
                billboard=True,
                color=color.yellow
            )

    def generate_drone(self, nb_drones):
        """Crée nb_drones sphères génériques (utilisé si pas de chemins assignés)."""
        for i in range(nb_drones):
            drone = Entity(
                model='sphere',
                color=color.black,
                scale=Vec3(0.5, 0.5, 0.5),
                position=Vec3(0, 3, 0)
            )
            self.drones.append(drone)

    def assign_paths_from_data(self, drone_data, speed=5.0):
        """
        Charge les chemins depuis la structure retournée par le parser.

        drone_data : liste de dicts avec 'id' et 'path'
        Exemple    : [
            {'id': 'drone_1', 'path': ['start', 'bottleneck', 'goal'], 'visited': [...]},
            ...
        ]
        """
        colors = [color.red, color.blue, color.orange, color.cyan,
                  color.magenta, color.lime, color.white, color.pink]

        for i, drone_info in enumerate(drone_data):
            drone_id = drone_info['id']
            path     = drone_info['path']

            # Filtre les hubs inconnus et dédoublonne les consécutifs
            clean_path = []
            for hub in path:
                if hub not in self.hub_positions:
                    continue
                # Supprime les doublons consécutifs (ex: ['start','start',...])
                if not clean_path or clean_path[-1] != hub:
                    clean_path.append(hub)

            if len(clean_path) < 2:
                continue

            # Crée l'entité drone positionné sur son hub de départ
            start_pos = self.hub_positions[clean_path[0]]
            drone_entity = Entity(
                model='sphere',
                color=colors[i % len(colors)],
                scale=Vec3(0.5, 0.5, 0.5),
                position=start_pos
            )
            # Étiquette flottante avec l'id du drone
            label = Text(
                text=drone_id,
                scale=6,
                billboard=True,
                color=colors[i % len(colors)],
                parent=drone_entity,
                y=1.4          # au-dessus de la sphère
            )

            self.drone_entities[drone_id] = drone_entity
            self.drone_states[drone_id] = {
                'entity':   drone_entity,
                'path':     clean_path,
                'seg_idx':  0,
                'progress': 0.0,
                'speed':    speed,
                'done':     False,
            }

    def _update_drones(self):
        # PASSE 1 : compte combien de drones occupent chaque hub
        hub_occupancy = {}  # hub_name -> nombre de drones présents ou en route

        for drone_id, state in self.drone_states.items():
            if state['done']:
                continue
            path    = state['path']
            seg_idx = state['seg_idx']
            if state['progress'] == 0.0:
                # Drone à l'arrêt : occupe son hub actuel
                if seg_idx < len(path):
                    hub = path[seg_idx]
                    hub_occupancy[hub] = hub_occupancy.get(hub, 0) + 1
            else:
                # Drone en transit : réserve sa destination
                if seg_idx + 1 < len(path):
                    hub = path[seg_idx + 1]
                    hub_occupancy[hub] = hub_occupancy.get(hub, 0) + 1

        # PASSE 2 : détermine quels drones peuvent bouger ce tick
        can_move = set()
        for drone_id, state in self.drone_states.items():
            if state['done']:
                continue
            if state['progress'] > 0.0:
                # Déjà en transit : continue toujours
                can_move.add(drone_id)
                continue
            path    = state['path']
            seg_idx = state['seg_idx']
            if seg_idx >= len(path) - 1:
                continue
            next_hub = path[seg_idx + 1]
            current_count = hub_occupancy.get(next_hub, 0)
            capacity      = self.hub_capacity.get(next_hub, 1)
            # Peut partir si le hub suivant n'est pas encore plein
            if current_count < capacity:
                can_move.add(drone_id)
                # Incrémente immédiatement pour les drones suivants dans cette passe
                hub_occupancy[next_hub] = current_count + 1

        # Debug
        if not hasattr(self, '_debug_timer'):
            self._debug_timer = 0
        self._debug_timer += time.dt
        if self._debug_timer >= 1.0:
            self._debug_timer = 0

        # PASSE 3 : déplace uniquement les drones autorisés
        for drone_id, state in self.drone_states.items():
            if state['done']:
                continue

            path    = state['path']
            seg_idx = state['seg_idx']

            if seg_idx >= len(path) - 1:
                state['done'] = True
                continue

            if drone_id not in can_move:
                continue

            start = self.hub_positions[path[seg_idx]]
            end   = self.hub_positions[path[seg_idx + 1]]
            dist  = (end - start).length()

            if dist == 0:
                state['seg_idx'] += 1
                state['progress'] = 0.0
                continue

            state['progress'] += (state['speed'] / dist) * time.dt

            if state['progress'] >= 1.0:
                state['seg_idx']  += 1
                state['progress']  = 0.0
                if state['seg_idx'] < len(path):
                    state['entity'].position = self.hub_positions[path[state['seg_idx']]]
            else:
                state['entity'].position = lerp(start, end, state['progress'])
                direction = (end - start).normalized()
                if direction.length() > 0:
                    state['entity'].look_at(state['entity'].position + direction)

    def generat_connections(self, connections):
        for zone1, zone2 in connections:
            name1 = zone1['name']
            name2 = zone2['name']
            if name1 in self.hub_positions and name2 in self.hub_positions:
                Entity(
                    model=Mesh(
                        vertices=(self.hub_positions[name1], self.hub_positions[name2]),
                        mode='line',
                        thickness=3
                    ),
                    color=color.white,
                    y=-3
                )


if __name__ == "__main__":
    parse = Parsing()
    algo = BFS()
    graph = Graphic(parse.pos, parse.zones)
    algo.parse_file()
    algo.build_adj()
    graph.generate_world()
    graph.generate_map()
    graph.generate_hub_labels()
    graph.generate_drone(parse.nb_drones)
    graph.generat_connections(parse.connections)
    graph.assign_paths_from_data(algo.path_for_drone(), speed=1.0)
    graph.run()
