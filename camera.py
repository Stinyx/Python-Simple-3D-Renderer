from vertex import *
import math 

class Camera:
    def __init__(self, FOV=90, near_clip=0.1, far_clip=1000):
        self.x = 0
        self.y = 0
        self.z = 0
        self.pitch = 0
        self.yaw = 0
        self.roll = 0
        self.FOV = FOV
        self.near_clip = near_clip
        self.far_clip = far_clip
        self.sensitivity = 0.8
        self.speed = 1
        
def handle_inputs(camera: Camera):
    sin = math.sin
    cos = math.cos
    pi = math.pi
    
    #SAVE MOUSE INFORMATION AND DELTA
    delta_time = get_frame_time()
    mouse_delta = get_mouse_delta()
    mouse_delta_x = mouse_delta.x
    mouse_delta_y = mouse_delta.y
    
    #PULL ATTRIBUTES INTO LOCAL (FASTER)
    pitch, yaw = camera.pitch, camera.yaw
    cx, cy, cz = camera.x, camera.y, camera.z
    sensitivity = camera.sensitivity
    cspeed = camera.speed
    speed = cspeed * delta_time

    #CALCULATE PITCH AND YAW
    yaw   -= mouse_delta_x * sensitivity * delta_time
    pitch += mouse_delta_y * sensitivity * delta_time
    
    #CLAMP PITCH SO YOU CANNOT LOOP OVER
    max_pitch = math.radians(89)
    pitch = max(-max_pitch, min(max_pitch, pitch))
    
    #PRECALCULATE TRIGONOMETRY FUNCTIONS
    sin_yaw = sin(yaw)
    cos_yaw = cos(yaw)
    sin_yaw_pi = sin(yaw - pi / 2)
    cos_yaw_pi = cos(yaw - pi / 2)

    #CALCULATE MOVEMENT VECTORS
    forward_x = -sin_yaw
    forward_z = cos_yaw
    right_x   = sin_yaw_pi
    right_z   = -cos_yaw_pi

    #FORWARD AND BACK
    if is_key_down(KEY_W):
        cx += forward_x * speed
        cz += forward_z * speed
    if is_key_down(KEY_S):
        cx -= forward_x * speed
        cz -= forward_z * speed

    #SIDE TO SIDE
    if is_key_down(KEY_A):
        cx += right_x * speed
        cz += right_z * speed
    if is_key_down(KEY_D):
        cx -= right_x * speed
        cz -= right_z * speed

    #UP AND DOWN
    if is_key_down(KEY_SPACE):
        cy -= speed
    if is_key_down(KEY_LEFT_CONTROL):
        cy += speed
    
    #ASSIGN LOCAL VARIABLES BACK TO CAMERA
    camera.x, camera.y, camera.z = cx, cy, cz
    camera.pitch, camera.yaw = pitch, yaw
        

        

        