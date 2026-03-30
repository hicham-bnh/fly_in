from ursina import Text, Ursina, color, Vec3, Sky
from ursina import EditorCamera, Entity, Mesh, time
from ursina import DirectionalLight, lerp
from ursina.prefabs.first_person_controller import FirstPersonController
from typing import Any, List, Dict


class Graphic:
    def __init__(self, position: Any, all_pos: Any) -> None:
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
        self.drones: List[Any] = []
        self.drone_entities: Dict[Any, Any] = {}
        self.all_pos = all_pos
        self.position = position
        self.hub_positions = {
            zone['name']: Vec3(zone['x'] * 2.5, 3, zone['y'] * 2.5)
            for zone in self.all_pos
        }
        self.drone_states: Dict[Any, Any] = {}
        self.hub_positions = {
            zone['name']: Vec3(zone['x'] * 2.5, 3, zone['y'] * 2.5)
            for zone in self.all_pos
        }
        self.hub_capacity = {
            zone['name']: zone['capacity']
            for zone in self.all_pos
        }
        self.is_moving = False
        instance_handler = Entity()
        instance_handler.input = self.input
        self.current_turn = 0

    def input(self, key: Any) -> None:
        if key == 'space' and not self.is_moving:
            self.current_turn += 1
            self.is_moving = True
        if key == 'escape':
            quit()

    def generate_world(self) -> None:
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

    def run(self) -> None:
        updater = Entity()
        updater.update = self._update_drones
        self.app.run()

    def generate_map(self) -> None:
        for a, b, col_data in self.position:
            if col_data == "purple":
                col_data = "violet"
            if col_data == "maroon":
                col_data = "brown"
            if col_data in ("darkred", "crimson"):
                col_data = "brown"
            clean_color = col_data
            if isinstance(col_data, str):
                clean_color = col_data.replace('[color=', '').replace(']', '')
            if hasattr(color, clean_color):
                final_color = getattr(color, clean_color)
            else:
                print("color invalide we take the white ase default")
                final_color = color.white
            Entity(
                model='cube',
                origin_y=-0.5,
                scale=Vec3(0.5, 0.5, 0.5),
                texture='brick',
                x=a * 2.5,
                z=b * 2.5,
                collider='box',
                color=final_color
            )

    def generate_hub_labels(self) -> None:
        for name, pos in self.hub_positions.items():
            Text(
                text=name,
                position=Vec3(pos.x, pos.y + 1.0, pos.z),
                scale=8,
                billboard=True,
                color=color.yellow
            )

    def generate_drone(self, nb_drones: int) -> None:
        for i in range(nb_drones):
            drone = Entity(
                model='sphere',
                color=color.black,
                scale=Vec3(0.5, 0.5, 0.5),
                position=Vec3(0, 3, 0)
            )
            self.drones.append(drone)

    def assign_paths_from_data(
            self,
            drone_data: Any,
            speed: float = 5.0
    ) -> None:
        colors = [color.red, color.blue, color.orange, color.cyan,
                  color.magenta, color.lime, color.white, color.pink]
        for i, drone_info in enumerate(drone_data):
            drone_id = drone_info['id']
            path = drone_info['path']
            if not path:
                continue
            start_pos = self.hub_positions[path[0]]
            drone_entity = Entity(
                model='sphere',
                color=colors[i % len(colors)],
                scale=Vec3(0.5, 0.5, 0.5),
                position=start_pos
            )
            Text(
                text=drone_id,
                scale=6,
                billboard=True,
                parent=drone_entity,
                y=1.4,
                color=drone_entity.color
            )
            self.drone_entities[drone_id] = drone_entity
            self.drone_states[drone_id] = {
                'entity':   drone_entity,
                'path':     path,
                'slot':     i
            }

    def _update_drones(self) -> None:
        if not self.is_moving:
            return
        all_stopped = True
        for drone_id, state in self.drone_states.items():
            path = state['path']
            idx = min(self.current_turn, len(path) - 1)
            target_name = path[idx]
            offset = Vec3(0, 0, 0)
            target_pos = self.hub_positions[target_name] + offset
            dist = (target_pos - state['entity'].position).length()
            if dist > 0.05:
                all_stopped = False
                state['entity'].position = lerp(
                    state['entity'].position,
                    target_pos, 15 * time.dt
                )
            else:
                state['entity'].position = target_pos
        if all_stopped:
            self.is_moving = False

    def generat_connections(self, connections: Any) -> None:
        for zone1, zone2 in connections:
            name1 = zone1['name']
            name2 = zone2['name']
            if name1 in self.hub_positions and name2 in self.hub_positions:
                Entity(
                    model=Mesh(
                        vertices=(
                            self.hub_positions[name1],
                            self.hub_positions[name2]
                        ),
                        mode='line',
                        thickness=3
                    ),
                    color=color.white,
                    y=-3
                )
