from pyray import *

class Edge:
    def __init__(self, vertex1, vertex2):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        
    def draw(self):
        draw_line(self.vertex1.x, self.vertex1.y, self.vertex2.x, self.vertex2.y, BLACK)