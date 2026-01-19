from vertex import Vertex
from pyray import *

points = []

points.append([200, 200])
points.append([300, 200])
points.append([300, 300])
points.append([200, 300])

window_width = 800
window_height = 450

points.reverse()

def handle_movement(object):
    
    x = 0
    y = 0
    dt = get_frame_time()
    speed = 100
    
    if is_key_down(KEY_W):
        y -= speed * dt
    if is_key_down(KEY_S):
        y += speed * dt 
    if is_key_down(KEY_D):
        x += speed * dt
    if is_key_down(KEY_A):
        x -= speed * dt
        
    
    for vertex in object:
        vertex[0] += x
        vertex[1] += y
        
    

init_window(window_width, window_height, "testing")
while not window_should_close():
    begin_drawing()


    clear_background(WHITE)
    handle_movement(points)
    draw_triangle_fan(points, len(points), RED)
    

    end_drawing()
    
close_window()



