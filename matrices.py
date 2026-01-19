import math
from vertex import *
from camera import *

'''
def rotate_y(point, angle):
    cos = math.cos
    sin = math.sin
    
    x, y, z = point
    c = cos(angle)
    s = sin(angle)
    return [x*c - z*s, y, x*s + z*c]

def rotate_x(point, angle):
    cos = math.cos
    sin = math.sin
    
    x, y, z = point
    c = cos(angle)
    s = sin(angle)
    return [x, y*c - z*s, y*s + z*c]

def subtract(vertices: Vertex, camera: Camera):
    return [vertices.x - camera.x, vertices.y - camera.y, vertices.z - camera.z]

def project(point, screen_w, screen_h, fov):
    tan = math.tan
    radians = math.radians
    
    x, y, z = point
    if z <= 0:
        return None  # behind camera

    f = screen_w / (2 * tan(radians(fov) / 2))

    screen_x = (x * f) / z + screen_w / 2
    screen_y = (y * f) / z + screen_h / 2

    return int(screen_x), int(screen_y)

def world_to_screen(point: Vertex, camera: Camera):
    # translate
    p = subtract(point, camera)

    # rotate
    p = rotate_y(p, -camera.yaw)
    p = rotate_x(p, camera.pitch)

    # project
    return project(p, 800, 450, camera.FOV)

'''

def world_to_screen(point: Vertex, camera: Camera, screen_w=800, screen_h=450, ox=0, oy=0, oz=0, scale=1, obj_yaw_dg=0, obj_roll_dg=0, obj_pitch_dg=0):
    cos = math.cos
    sin = math.sin
    radians = math.radians
    
    px, py, pz = point.x, point.y, point.z
    cx, cy, cz = camera.x, camera.y, camera.z
    yaw = camera.yaw
    pitch = camera.pitch
    
    # Convert degrees to radians
    obj_pitch = radians(obj_pitch_dg)
    obj_yaw   = radians(obj_yaw_dg)
    obj_roll  = radians(obj_roll_dg)
    
    # --- OBJECT ROTATION (local space) ---
    # Roll (Z axis)
    c, s = cos(obj_roll), sin(obj_roll)
    x = px * c - py * s
    y = px * s + py * c
    z = pz

    # Pitch (X axis)
    c, s = cos(obj_pitch), sin(obj_pitch)
    y2 = y * c - z * s
    z2 = y * s + z * c
    y, z = y2, z2

    # Yaw (Y axis)
    c, s = cos(obj_yaw), sin(obj_yaw)
    x2 = x * c - z * s
    z2 = x * s + z * c
    x, z = x2, z2

    # --- SCALE ---
    x *= scale
    y *= scale
    z *= scale

    # --- TRANSLATE TO CAMERA SPACE ---
    x = x + ox - cx
    y = y + oy - cy
    z = z + oz - cz
    
    # CAMERA ROTATION
    cos_y = cos(-yaw)
    sin_y = sin(-yaw)
    cos_p = cos(pitch)
    sin_p = sin(pitch)
    
    xz = x * cos_y - z * sin_y
    zz = x * sin_y + z * cos_y
    
    yz = y * cos_p - zz * sin_p
    zz = y * sin_p + zz * cos_p
    
    # BEHIND CAMERA CHECK
    if zz <= camera.near_clip:
        #zz = camera.near_clip 
        return None
    
    # PROJECT
    f = screen_w / (2 * math.tan(math.radians(camera.FOV) * 0.5))
    #     f = screen_w / (2 * math.tan(camera.FOV * 0.5)) idk chat gpt said this was wrong
    screen_x = (xz * f) / zz + screen_w * 0.5
    screen_y = (yz * f) / zz + screen_h * 0.5
    
    return screen_x, screen_y