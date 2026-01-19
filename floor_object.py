from vertex import *
from face import *
from object import Object

class Floor(Object):
    def __init__(self, width=20, depth=20, divisions=1, y=20, color=(150, 150, 150)):
        """
        Creates a flat floor as an Object.

        width, depth: total size along X/Z
        divisions: number of quads per axis (1 = single quad)
        y: height of the floor
        color: RGB color tuple for all faces
        """
        super().__init__()
        dx = width / divisions
        dz = depth / divisions
        start_x = -width / 2
        start_z = -depth / 2

        for i in range(divisions):
            for j in range(divisions):
                # Four corners of this quad
                x0 = start_x + i * dx
                x1 = start_x + (i + 1) * dx
                z0 = start_z + j * dz
                z1 = start_z + (j + 1) * dz

                v0 = Vertex(x0, y, z0)
                v1 = Vertex(x1, y, z0)
                v2 = Vertex(x1, y, z1)
                v3 = Vertex(x0, y, z1)

                idx = len(self.vertices)
                self.vertices += [v0, v1, v2, v3]

                # Two triangles per quad
                f1 = Face()
                f1.face_vertices = [idx, idx+1, idx+2]
                f1.vertices = [v0, v1, v2]
                f1.color = color

                f2 = Face()
                f2.face_vertices = [idx, idx+2, idx+3]
                f2.vertices = [v0, v2, v3]
                f2.color = color

                self.faces += [f1, f2]

    def draw(self, camera, draw_vertices=False):
        """
        Draws the floor using your Object.draw method.
        The floor is always drawn with triangles, no triangle fan.
        """
        super().draw(scale=1, x=0, y=1, z=0, rx=0, ry=0, rz=0, camera=camera, draw_vertices=draw_vertices, draw_faces=True)