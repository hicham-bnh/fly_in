from ursina import Ursina, color, Vec3, sys, \
    BoxCollider, EditorCamera, Mesh, DirectionalLight, Sky
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from parsing import Parsing
from ursina import Entity, distance, time
import random
from algo import BFS


class DroneDecor(Entity):
    def __init__(self, name, path_names, hub_positions):
        super().__init__(
            model='sphere',
            color=color.black,
            scale=Vec3(0.5, 0.5, 0.5),
            position=hub_positions[path_names[0]] + Vec3(0, 3, 0)
        )
        self.name = name
        self.start_y = self.y
        self.path_names = path_names
        self.hub_positions = hub_positions
        self.current_step = 0
        self.speed = 2.5
        self.timer = 0
        self.delay = 5.0
        

    def update(self):
        if self.timer < self.delay:
                self.timer += time.dt
                return
        if self.current_step < len(self.path_names):
            target_hub = self.path_names[self.current_step]
            target_pos = self.hub_positions[target_hub] + Vec3(0, 3, 0)
            if distance(self.position, target_pos) > 0.1:
                direction = (target_pos - self.position).normalized()
                self.position += direction * self.speed * time.dt
            else:
                self.current_step += 1


class DroneSimulation:
    def __init__(self):
        self.app = Ursina(title="fly-in")
        random.seed(0)
        Entity.default_shader = lit_with_shadows_shader
        self.parser = Parsing()
        self.algo = BFS()
        self.parser.read_file(sys.argv[len(sys.argv) - 1])
        self.parser.check_line()
        self.parser.parse()
        self.algo.parse_file(sys.argv[len(sys.argv) - 1])
        self.algo.get_path()
        self.drones_entities = []
        nb_drone = self.parser.nb_drones
        self.hub_positions = {
            zone['name']: Vec3(zone['x'] * 2.5, 0.1, zone['y'] * 2.5)
            for zone in self.parser.zones
        }
        self.create_world()
        self.generate_map(self.parser.pos)
        self.generate_network_lines()
        self.player = FirstPersonController(
            z=-0.1,
            origin_y=1,
            speed=20,
            gravity=0,
            y=4
        )
        self.player.collider = BoxCollider(
            self.player, Vec3(0, 1, 0), Vec3(1, 2, 1)
        )
        self.editor_camera = EditorCamera(enabled=False, ignore_paused=True)
        algo_path = self.algo.get_path_all_drone()
        for drone_dict in algo_path:
            for d_name, d_path in drone_dict.items():
                new_drone = DroneDecor(
                    name=d_name, 
                    path_names=d_path, 
                    hub_positions=self.hub_positions,
            )
                self.drones_entities.append(new_drone)

    def generate_network_lines(self):
        all_vertices = []
        for zone1_dict, zone2_dict in self.parser.connections:
            name1 = zone1_dict['name']
            name2 = zone2_dict['name']
            if name1 in self.hub_positions and name2 in self.hub_positions:
                all_vertices.append(self.hub_positions[name1])
                all_vertices.append(self.hub_positions[name2])
        if all_vertices:
            self.network = Entity(
                model=Mesh(vertices=all_vertices, mode='line', thickness=3),
                color=color.white,
                z=-0.01
            )

    def create_world(self):
        self.ground = Entity(
            model='plane',
            collider='box',
            scale=Vec3(110),
            texture='grass',
            texture_scale=(4, 4)
        )
        self.sun = DirectionalLight()
        self.sun.look_at(Vec3(1, -1, -1))
        Sky()

    def generate_map(self, positions):
        self.obstacles_parent = Entity()
        for a, b, col_data in positions:
            if col_data == "purple":
                col_data = "violet"
            if col_data == "maroon":
                col_data = "brown"
            if col_data == "darkred" or col_data == "crimson":
                col_data = "brown"
            clean_color = col_data
            if isinstance(col_data, str):
                clean_color = col_data.replace('[color=', '').replace(']', '')
            Entity(
                parent=self.obstacles_parent,
                model='cube',
                origin_y=-0.5,
                scale=Vec3(0.5, 0.5, 0.5),
                texture='brick',
                x=a * 2.5,
                z=b * 2.5,
                collider='box',
                color=getattr(color, clean_color)
                        if hasattr(color, clean_color) else color.white
            )

    def run(self):
        self.app.run()


def input(key):
    if key == 'escape':
        quit()



if __name__ == '__main__':
    sim = DroneSimulation()
    sim.run()