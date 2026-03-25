from ursina import *
from parsing import Parsing
from ursina.prefabs.first_person_controller import FirstPersonController


class Graphic:
    def __init__(self):
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

    def generate_map(self, positions):
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
                model='cube',
                origin_y = -0.5,
                scale=Vec3(0.5, 0.5, 0.5),
                texture='brick',
                x = a * 2.5,
                z = b * 2.5,
                collider='box',
                color=getattr(color, clean_color) if hasattr(color,clean_color) else color.white
            )


if __name__ == "__main__":
    parse = Parsing()
    graph = Graphic()
    graph.generate_world()
    graph.generate_map(parse.pos)
    graph.run()
