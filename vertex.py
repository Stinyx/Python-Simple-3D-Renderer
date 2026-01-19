from pyray import *

class Vertex:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        
    def draw(self, scale=100, x=400, y=225, debug=False):
        screen_x = int(self.x * scale + x)
        screen_y = int(-self.y * scale + y)
        
        draw_circle(screen_x, screen_y, 1, BLACK)
        
        if debug:
            draw_text(f"({self.x}, {self.y}, {self.z})\n({screen_x}, {screen_y})", screen_x + 5, screen_y - 5, 10, RED)
        
        