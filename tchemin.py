from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from parsing import Parsing
import random

class DroneSimulation:
    def __init__(self):
        # 1. Initialisation du moteur
        self.app = Ursina(title="fly-in")
        random.seed(0)
        Entity.default_shader = lit_with_shadows_shader

        # 2. Chargement des données (Ton module Parsing)
        self.parser = Parsing()
        self.parser.read_file(sys.argv[len(sys.argv) - 1])
        self.parser.check_line()
        self.parser.parse()
        # 3. Création de l'environnement
        self.create_world()
        self.generate_map(self.parser.pos)
        
        # 4. Configuration du Joueur / Drone
        self.player = FirstPersonController(
            model='cube', 
            z=-10, 
            color=color.orange, 
            origin_y=-.5, 
            speed=8, 
            collider='box'
        )
        self.player.collider = BoxCollider(self.player, Vec3(0,1,0), Vec3(1,2,1))
        
        # Caméra de debug
        self.editor_camera = EditorCamera(enabled=False, ignore_paused=True)

    def create_world(self):
        """Crée le sol, la lumière et le ciel."""
        self.ground = Entity(
            model='plane', 
            collider='box', 
            scale=100, 
            texture='grass', 
            texture_scale=(4,4)
        )
        self.sun = DirectionalLight()
        self.sun.look_at(Vec3(1,-1,-1))
        Sky()

    def generate_map(self, positions):
        """Génère les obstacles à partir des positions parsées."""
        # On peut créer un parent vide pour regrouper les obstacles
        self.obstacles_parent = Entity()
        
        for a, b, col_data in positions:

            clean_color = col_data
            if isinstance(col_data, str):
                clean_color = col_data.replace('[color=', '').replace(']', '')
            Entity(
                parent=self.obstacles_parent, # Fix: self.obstacles_parent au lieu de self
                model='cube',
                origin_y=-0.5,
                scale=(0.5, 0.5, 0.5),
                texture='brick',
                x=a * 2.0,
                z=b * 2.0,
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

