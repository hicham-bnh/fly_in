from ursina import Ursina, color, Vec3, sys, \
    BoxCollider, EditorCamera, Mesh, DirectionalLight, Sky
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from parsing import Parsing
from ursina import Entity
import random


class DroneDecor(Entity):
    def __init__(self, name, position=(0, 2, 0)):
        super().__init__(
            model='sphere',
            color=color.black,
            scale=Vec3(0.5, 0.5, 0.5),
            position=position
        )
        self.name = name
        self.start_y = self.y


class DroneSimulation:
    def __init__(self):
        self.app = Ursina(title="fly-in")
        random.seed(0)
        Entity.default_shader = lit_with_shadows_shader
        self.parser = Parsing()
        self.parser.read_file(sys.argv[len(sys.argv) - 1])
        self.parser.check_line()
        self.parser.parse()
        self.drones = {}
        nb_drone = self.parser.nb_drones
        self.hub_positions = {
            zone[0]: Vec3(zone[1] * 2.5, 0.1, zone[2] * 2.5)
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
        for i in range(nb_drone):
            self.mon_drone_visuel = DroneDecor(
                f"drone_{i+1}", position=(0, 3, 0)
            )
            drone = {
                f"drone_0{i+1}": None
            }
            self.drones.update(drone)

    def generate_network_lines(self):
        all_vertices = []
        for zone1, zone2 in self.parser.connections:
            if zone1 in self.hub_positions and zone2 in self.hub_positions:
                all_vertices.append(self.hub_positions[zone1])
                all_vertices.append(self.hub_positions[zone2])
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
