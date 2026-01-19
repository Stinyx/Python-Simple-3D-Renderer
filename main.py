from pyray import *
from floor_object import *
from camera import *
from object import load_object, draw_object_statistics


fulscreen = False

window_width = 800
window_height = 450

spinning_fish = load_object('Assets/fishClown.obj')
cube = load_object('Assets/testcube.obj')
grid_floor = Floor(width=50, depth=50, divisions=10, y=0, color=(120, 120, 120))

camera = Camera(FOV=100, near_clip=0.1, far_clip=1000)
angle = 0
rotation_speed = 5

init_window(window_width, window_height, "Stinyx's Renderer Engine")
disable_cursor()

if fulscreen:
    toggle_fullscreen()

while not window_should_close():
    
    begin_drawing()
    clear_background(WHITE)
    handle_inputs(camera)
    
    angle += rotation_speed
    if angle > 360:
        angle = 0
    
    grid_floor.draw(camera=camera)

    cube.draw(camera=camera, scale=0.1, x=1.2, y=0, z=0, rx=0, ry=0, rz=0, draw_vertices=False, draw_faces=True, draw_edges=False)
    spinning_fish.draw(camera=camera, scale=0.1, x=0, y=0, z=0, rx=0, ry=angle, rz=0, draw_vertices=False, draw_faces=True, draw_edges=False)
    
    
    draw_object_statistics(spinning_fish)
    draw_text("FISH", int(window_width/2 - measure_text("FISH", 50)/2), 20, 50, BLACK)
    end_drawing()
    
    set_window_title(f"[Stinyx's Renderer] FPS: {get_fps()}")
close_window()

