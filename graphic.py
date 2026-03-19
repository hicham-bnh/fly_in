from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from parsing import Parsing
import random

class DroneDecor(Entity):
    def __init__(self, name ,position=(0,2,0)):
        super().__init__(
            model='cube',
            color=color.black,
            scale=Vec3(1, 0.2, 1),
            position=position
        )
        self.name = name
        Entity(parent=self, model='cube', color=color.dark_gray, scale=Vec3(1.2, 0.1, 0.1), rotation_y=45)
        Entity(parent=self, model='cube', color=color.dark_gray, scale=Vec3(1.2, 0.1, 0.1), rotation_y=-45)
        self.props = []
        for p in [(-.5,.1,-.5), (.5,.1,-.5), (-.5,.1,.5), (.5,.1,.5)]:
            prop = Entity(parent=self, model='cube', color=color.red, scale=Vec3(.4,.02,.05), position=p)
            self.props.append(prop)
        self.start_y = self.y
        self.t = 0

    def update(self):
        for p in self.props:
            p.rotation_y += 1000 * time.dt
        self.t += time.dt
        self.y = self.start_y + math.sin(self.t * 2) * 0.2
        self.rotation_z = math.cos(self.t) * 2
        self.rotation_x = math.sin(self.t * 1.5) * 2

class DroneSimulation:
    def __init__(self):
        self.app = Ursina(title="fly-in")
        random.seed(0)
        Entity.default_shader = lit_with_shadows_shader
        self.parser = Parsing()
        self.parser.read_file(sys.argv[len(sys.argv) - 1])
        self.parser.check_line()
        self.parser.parse()
        nb_drone = self.parser.nb_drones
        self.hub_positions = {
        zone[0]: Vec3(zone[1] * 2.5, 0.1, zone[2] * 2.5) 
        for zone in self.parser.zones
        }
        self.create_world()
        self.generate_map(self.parser.pos)
        self.generate_network_lines()
        self.player = FirstPersonController(
            model='cube', 
            z=-10, 
            color=color.orange, 
            origin_y=-.5, 
            speed=8, 
            collider='box'
        )
        self.player.collider = BoxCollider(self.player, Vec3(0,1,0), Vec3(1,2,1))
        self.editor_camera = EditorCamera(enabled=False, ignore_paused=True)
        for i in range(nb_drone):
            self.mon_drone_visuel = DroneDecor(f"drone_{i+1}", position=(0, 3, 0))

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
            scale=Vec3(150), 
            texture='grass', 
            texture_scale=(4,4)
        )
        self.sun = DirectionalLight()
        self.sun.look_at(Vec3(1,-1,-1))
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
                color = getattr(color, clean_color) if hasattr(color, clean_color) else color.white
            )

    def input(self, key):
        """Gestion des touches (Pause / Tab)."""
        if key == 'tab':
            self.editor_camera.enabled = not self.editor_camera.enabled
            self.player.visible_self = self.editor_camera.enabled
            self.player.cursor.enabled = not self.editor_camera.enabled
            mouse.locked = not self.editor_camera.enabled
            self.editor_camera.position = self.player.position
            application.paused = self.editor_camera.enabled
        
        if key == 'escape':
            application.quit()

    def run(self):
        self.app.run()




if __name__ == '__main__':
    sim = DroneSimulation()
    sim.run()

