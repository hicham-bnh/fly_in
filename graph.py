from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# --- TES DONNÉES ---
NODES = [
    ('start', 0, 0, color.green),
    ('waypoint1', 1, 0, color.blue),
    ('waypoint2', 2, 0, color.blue),
    ('goal', 3, 0, color.red)
]

EDGES = [
    ('start', 'waypoint1', 1),
    ('waypoint1', 'waypoint2', 1),
    ('waypoint2', 'goal', 1)
]

class Waypoint(Entity):
    def __init__(self, name, x, z, node_color):
        super().__init__(
            model='sphere',
            color=node_color,
            position=(x * 5, 0.5, z * 5),
            scale=1
        )
        self.label = Text(text=name, parent=self, y=1.5, billboard=True, scale=10)

class DroneSim:
    def __init__(self):
        self.app = Ursina()
        
        # 1. Fond et Lumière
        window.color = color.black
        Sky()
        DirectionalLight(y=10, rotation=(45, 45, 0))

        # 2. Sol de sécurité (très large et coloré pour être sûr de le voir)
        self.ground = Entity(model='plane', scale=50, texture='grid', color=color.dark_gray, collider='box')

        # 3. Tes points (on s'assure qu'ils existent)
        self.waypoints = {}
        for name, x, z, n_color in NODES:
            # On force une position visible
            wp = Waypoint(name, x, z, n_color)
            self.waypoints[name] = wp
            print(f"Point {name} créé à {wp.position}")

        # 4. Liens
        for start_node, end_node, weight in EDGES:
            self.draw_edge(start_node, end_node)
        
        # 5. JOUEUR : On le place en hauteur pour qu'il voit tout d'en haut
        self.player = FirstPersonController(position=(0, 0, -20), speed=10)
        self.player.look_at(self.waypoints['start']) # Force à regarder le début

    # ... (garde ta fonction draw_edge)

    def run(self):
        self.app.run()

    def draw_edge(self, start_name, end_name):
        # 1. Récupérer les positions mondiales (world_position)
        start_pos = self.waypoints[start_name].world_position
        end_pos = self.waypoints[end_name].world_position
        
        # 2. Calculer la distance réelle
        dist = distance(start_pos, end_pos)
        
        # 3. Créer l'arête
        edge = Entity(
            model='cube',
            # On place le centre de l'entité pile au milieu
            position=(start_pos + end_pos) / 2,
            # On demande à l'axe Z de pointer vers la fin
            look_at=end_pos,
            # X et Y sont l'épaisseur, Z est la longueur
            scale=(0.1, 0.1, dist),
            color=color.white,
            shader=None # Désactiver les ombres peut aider à mieux voir l'alignement
        )

    def run(self):
        self.app.run()

# Gestion des inputs (doit être au niveau global pour Ursina)
def input(key):
    if key == 'escape':
        application.quit()

if __name__ == '__main__':
    sim = DroneSim()
    sim.run()