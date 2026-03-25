from ursina import *
from parsing import Parsing
from ursina.prefabs.first_person_controller import FirstPersonController


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
        self.all_pos = all_pos
        self.position = position
        self.hub_positions = {
            zone['name']: Vec3(zone['x'] * 2.5, 3, zone['y'] * 2.5)
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
        self.app.run()

    def generate_map(self):
        for a, b, col_data in self.position:
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
                model='cube',
                origin_y = -0.5,
                scale=Vec3(0.5, 0.5, 0.5),
                texture='brick',
                x = a * 2.5,
                z = b * 2.5,
                collider='box',
                color=getattr(color, clean_color) if hasattr(color,clean_color) else color.white
            )

    def generate_drone(self, nb_drones):
        for i in range(nb_drones):
            drone = Entity(
                model='sphere',
                color = color.black,
                scale=Vec3(0.5, 0.5, 0.5),
                position=Vec3(0, 3, 0)
            )
            self.drones.append(drone)


if __name__ == "__main__":
    parse = Parsing()
    graph = Graphic(parse.pos, parse.zones)
    graph.generate_world()
    graph.generate_map()
    graph.generate_drone(parse.nb_drones)
    graph.run()
