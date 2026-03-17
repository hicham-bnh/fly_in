import pyray as rl
import math
 
rl.init_window(3840, 2160, "Fly-in")
rl.set_target_fps(80)
 
camera = rl.Camera3D(
    rl.Vector3(0.0, 1.8, 0.0),
    rl.Vector3(1.0, 1.8, 0.0),
    rl.Vector3(0.0, 1.0, 0.0),
    70.0,
    rl.CAMERA_PERSPECTIVE
)
 
rl.disable_cursor()

suny = rl.load_texture("/home/mobenhab/Downloads/mich-removebg-preview.png")
texture_michel = rl.load_texture("/home/mobenhab/Downloads/IMG_20250827_194943-removebg-preview.png")
drone = rl.load_texture("/home/mobenhab/Downloads/icon128.png")
 
def draw_michel_tournant(x, z, texture):
    pos = rl.Vector3(float(x), 1.5, float(z))
    rl.draw_billboard_rec(
        camera, texture,
        rl.Rectangle(0, 0, texture.width, texture.height),
        pos,
        rl.Vector2(3.0, 3.0),
        rl.WHITE
    )
 
arbres = [(5,5), (7,7), (-4,3), (11,11), (2,-6), (-7,-2), (8,-4), (-3,7), (6,2), (-6,-6), (1,8), (9,9)]
 
vaches = [
    {"x": 0.0,  "y": 2.0, "z": 3.0,  "vitesse": 0.015, "rayon": 4.0, "angle": 0.0},
    {"x": -5.0, "y": 2.0, "z": -5.0, "vitesse": 0.015, "rayon": 5.0, "angle": 2.0},
    {"x": 7.0,  "y": 2.0, "z": 2.0,  "vitesse": 0.015, "rayon": 3.0, "angle": 4.0},
]
 
while not rl.window_should_close():
    rl.update_camera(camera, rl.CAMERA_FIRST_PERSON)
    t = rl.get_time()
 
    for vache in vaches:
        vache["angle"] += vache["vitesse"]
        vache["x"] = math.cos(vache["angle"]) * vache["rayon"]
        vache["z"] = math.sin(vache["angle"]) * vache["rayon"]
        vache["y"] = 2.0 + math.sin(t * 1.5 + vache["angle"]) * 0.3
 
    rl.begin_drawing()
    rl.clear_background(rl.SKYBLUE)
    rl.begin_mode_3d(camera)
 
    rl.draw_plane(rl.Vector3(0, 0, 0), rl.Vector2(40, 40), rl.DARKGREEN)
    rl.draw_grid(40, 1.0)
 
    # Michel à la place des arbres
    for (x, z) in arbres:
        draw_michel_tournant(x, z, texture_michel)
 
    # Rochers décoratifs
    for (x, z, s) in [(3,-3,0.5), (-5,6,0.7), (7,-7,0.4), (-8,1,0.6)]:
        rl.draw_sphere(rl.Vector3(float(x), s/2, float(z)), s, rl.GRAY)
 
    # Maison
    rl.draw_cube(rl.Vector3(-3.0, 1.0, -3.0), 3.0, 2.0, 3.0, rl.BEIGE)
    rl.draw_cube_wires(rl.Vector3(-3.0, 1.0, -3.0), 3.0, 2.0, 3.0, rl.BROWN)
    rl.draw_cylinder(rl.Vector3(-3.0, 2.0, -3.0), 0.0, 2.2, 1.5, 4, rl.MAROON)
    rl.draw_billboard(camera, suny, rl.Vector3(-3.0, 1.0, -3.0), 2.0, rl.WHITE)
 
    # Michel volants
    for vache in vaches:
        pos = rl.Vector3(vache["x"], vache["y"], vache["z"])
        rl.draw_billboard(camera, drone, pos, 3.0, rl.WHITE)
        rl.draw_line_3d(
            pos,
            rl.Vector3(vache["x"], 0.0, vache["z"]),
            rl.fade(rl.WHITE, 0.3)
        )
 
    rl.end_mode_3d()
 
    # HUD
    rl.draw_text("ZQSD : se déplacer | Souris : regarder | ESC : quitter", 10, 10, 16, rl.WHITE)
    rl.draw_text(f"Vaches volantes : {len(vaches)}", 10, 30, 16, rl.WHITE)
    rl.draw_text(f"Michel(s) dans le pré : {len(arbres)}", 10, 50, 16, rl.WHITE)
 
    # Viseur
    cx, cy = 400, 300
    rl.draw_line(cx - 10, cy, cx + 10, cy, rl.WHITE)
    rl.draw_line(cx, cy - 10, cx, cy + 10, rl.WHITE)
 
    rl.end_drawing()
 
rl.unload_texture(texture_michel)
rl.unload_texture(drone)
rl.close_window()