from pyray import *
from camera import *
from vertex import *

import math

class Face:
    def __init__(self):
        self.face_vertices = []
        self.vertices = []
        self.color = (get_random_value(50, 255), get_random_value(50, 255), get_random_value(50, 255), 255)

'''
    def draw(self, scale=100, x=400, y=225):
        points = []
        for vertex in self.vertices:
            screen_x = int(vertex.x * scale + x)
            screen_y = int(-vertex.y * scale + y)
            points.append(Vector2(screen_x, screen_y))

        draw_triangle_fan(points, len(points), self.color)
'''  
 
def face_depth_face_average(face: Face, camera: Camera, obj_pitch_dg=0, obj_yaw_dg=0, obj_roll_dg=0, scale=1):
    vertices = face.vertices
    total_z = 0
    cos = math.cos
    sin = math.sin
    yaw = camera.yaw
    pitch = camera.pitch

    cx, cy, cz = camera.x, camera.y, camera.z

    cos_y = cos(-yaw)
    sin_y = sin(-yaw)
    cos_p = cos(pitch)
    sin_p = sin(pitch)

    # Convert object rotation from degrees to radians
    op = math.radians(obj_pitch_dg)
    oy = math.radians(obj_yaw_dg)
    oroll = math.radians(obj_roll_dg)

    cos_op, sin_op = cos(op), sin(op)
    cos_oy, sin_oy = cos(oy), sin(oy)
    cos_or, sin_or = cos(oroll), sin(oroll)

    for vertex in vertices:
        # --- Object rotation + scale ---
        x = vertex.x * cos_or - vertex.y * sin_or  # Roll
        y = vertex.x * sin_or + vertex.y * cos_or
        z = vertex.z

        y2 = y * cos_op - z * sin_op  # Pitch
        z2 = y * sin_op + z * cos_op
        y, z = y2, z2

        x2 = x * cos_oy - z * sin_oy  # Yaw
        z2 = x * sin_oy + z * cos_oy
        x, z = x2 * scale, z2 * scale
        y *= scale

        # --- Translate to camera space ---
        x -= cx
        y -= cy
        z -= cz

        # --- Camera rotation ---
        xz = x * cos_y - z * sin_y
        zz = x * sin_y + z * cos_y

        yz = y * cos_p - zz * sin_p
        zz = y * sin_p + zz * cos_p

        total_z += zz

    return total_z / len(vertices)


def face_depth_face_max(face: Face, camera: Camera):
    vertices = face.vertices
    max_z = -float('inf')  # use maximum camera-space Z instead of average
    cos = math.cos
    sin = math.sin
    yaw = camera.yaw
    pitch = camera.pitch

    cx, cy, cz = camera.x, camera.y, camera.z

    cos_y = cos(-yaw)
    sin_y = sin(-yaw)
    cos_p = cos(pitch)
    sin_p = sin(pitch)

    for vertex in vertices:
        # Translate to camera space
        x = vertex.x - cx
        y = vertex.y - cy
        z = vertex.z - cz

        # Rotate around Y (yaw)
        xz = x * cos_y - z * sin_y
        zz = x * sin_y + z * cos_y

        # Rotate around X (pitch)
        yz = y * cos_p - zz * sin_p
        zz = y * sin_p + zz * cos_p  # camera-space Z

        # Take the maximum Z for depth
        if zz > max_z:
            max_z = zz

    return max_z