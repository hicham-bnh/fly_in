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

arbres = [(5,5), (-4,3), (2,-6), (-7,-2), (8,-4), (-3,7), (6,2), (-6,-6), (1,8), (9,9)]
drones = [
    {"x": 3.0,  "y": 4.0, "z": 3.0,  "vitesse": 0.02, "rayon": 4.0, "angle": 0.0,   "couleur": rl.RED},
    {"x": -5.0, "y": 6.0, "z": -5.0, "vitesse": 0.015,"rayon": 5.0, "angle": 2.0,   "couleur": rl.BLUE},
    {"x": 7.0,  "y": 3.0, "z": 2.0,  "vitesse": 0.03, "rayon": 3.0, "angle": 4.0,   "couleur": rl.YELLOW},
]

def draw_drone(x, y, z, couleur):
    """Dessine un drone : corps central + 4 bras + 4 rotors"""
    cx, cy, cz = float(x), float(y), float(z)
    rl.draw_cube(rl.Vector3(cx, cy, cz), 0.3, 0.1, 0.3, couleur)
    bras = [
        (cx + 0.4, cz),
        (cx - 0.4, cz),
        (cx, cz + 0.4),
        (cx, cz - 0.4),
    ]
    for bx, bz in bras:
        rl.draw_cube(rl.Vector3((cx + bx) / 2, cy, (cz + bz) / 2), 0.35, 0.05, 0.05 if bx != cx else 0.35, rl.DARKGRAY)
    rotors = [
        (cx + 0.4, cz),
        (cx - 0.4, cz),
        (cx,       cz + 0.4),
        (cx,       cz - 0.4),
    ]
    for rx, rz in rotors:
        rl.draw_cylinder(rl.Vector3(rx, cy + 0.05, rz), 0.18, 0.18, 0.03, 8, rl.LIGHTGRAY)
    t = rl.get_time()
    led_color = rl.GREEN if int(t * 4) % 2 == 0 else rl.DARKGREEN
    rl.draw_sphere(rl.Vector3(cx, cy - 0.08, cz), 0.05, led_color)


while not rl.window_should_close():
    rl.update_camera(camera, rl.CAMERA_FIRST_PERSON)
    t = rl.get_time()
    for drone in drones:
        drone["angle"] += drone["vitesse"]
        drone["x"] = math.cos(drone["angle"]) * drone["rayon"]
        drone["z"] = math.sin(drone["angle"]) * drone["rayon"]
        drone["y"] = drone["y"] + math.sin(t * 2 + drone["angle"]) * 0.002
    rl.begin_drawing()
    rl.clear_background(rl.SKYBLUE)
    rl.begin_mode_3d(camera)
    rl.draw_plane(rl.Vector3(0, 0, 0), rl.Vector2(40, 40), rl.DARKGREEN)
    rl.draw_grid(40, 1.0)
    for (x, z) in arbres:
        rl.draw_cylinder(rl.Vector3(float(x), 0.0, float(z)), 0.2, 0.2, 2.0, 8, rl.BROWN)
        rl.draw_sphere(rl.Vector3(float(x), 2.8, float(z)), 1.1, rl.LIME)
    for (x, z, s) in [(3,-3,0.5), (-5,6,0.7), (7,-7,0.4), (-8,1,0.6)]:
        rl.draw_sphere(rl.Vector3(float(x), s/2, float(z)), s, rl.GRAY)
    rl.draw_cube(rl.Vector3(-3.0, 1.0, -3.0), 3.0, 2.0, 3.0, rl.BEIGE)
    rl.draw_cube_wires(rl.Vector3(-3.0, 1.0, -3.0), 3.0, 2.0, 3.0, rl.BROWN)
    rl.draw_cylinder(rl.Vector3(-3.0, 2.0, -3.0), 0.0, 2.2, 1.5, 4, rl.MAROON)
    for drone in drones:
        draw_drone(drone["x"], drone["y"], drone["z"], drone["couleur"])
        rl.draw_line_3d(
            rl.Vector3(drone["x"], drone["y"], drone["z"]),
            rl.Vector3(drone["x"], 0.0, drone["z"]),
            rl.fade(drone["couleur"], 0.3)
        )

    rl.end_mode_3d()
    rl.draw_text("ZQSD : se deplacer | Souris : regarder | ESC : quitter", 10, 10, 16, rl.WHITE)
    rl.draw_text(f"Drones actifs : {len(drones)}", 10, 30, 16, rl.WHITE)
    cx, cy = 400, 300
    rl.draw_line(cx - 10, cy, cx + 10, cy, rl.WHITE)
    rl.draw_line(cx, cy - 10, cx, cy + 10, rl.WHITE)

    rl.end_drawing()

rl.close_window()