from vertex import *
from face import *
from edge import *
from camera import *
from matrices import *

scene_objects = []

class Object:
    def __init__(self):
        self.path = ""
        self.vertices = []
        self.faces = []
        self.edges = []
        self.quad_count = 0
        self.tri_count = 0
        self.ngon_count = 0
        self.depth_average = 0
        
    def draw(self, scale, x, y, z, rx, ry, rz, camera,  draw_vertices=False, draw_faces=True, draw_edges=False):
        
        object_vertices = self.vertices
        object_faces = self.faces
       
        projected_points = []

        # IDK WHAT HAPPEND HERE BUT POINT TO SCREEN TRAINSLATION
        appendpoints = projected_points.append
        for vertex in object_vertices:    
            projected = world_to_screen(vertex, camera, ox=x, oy=y, oz=z, scale=scale, obj_pitch_dg=rx, obj_roll_dg=rz, obj_yaw_dg=ry)
            appendpoints(projected)
        
        # DRAW VERTICES
        if draw_vertices:
            for vertex in projected_points:
                if vertex is not None: 
                    if vertex[0] < 800 and vertex[0] > 0 and vertex[1] < 450 and vertex[1] > 0:
                        draw_circle(vertex[0], vertex[1], 2, BLACK)

        # GET DEPTH INFO ABOUT FACES
        face_depths = []
        total_depth = 0
        for face in self.faces:
            if face is not None:
                depth = face_depth_face_average(face, camera, obj_pitch_dg=rx, obj_roll_dg=rz, obj_yaw_dg=ry)
                total_depth += depth
                face_depths.append((depth, face))
        
        # SORT FACES BACK -> FRONT (PAINTERS ALGORITHM SIMILARLY)
        face_depths.sort(key=lambda f: f[0], reverse=True)
        self.depth_average = total_depth / len(self.faces)


        if draw_faces:
            for _, face in face_depths:
                points = []

                for i in face.face_vertices:
                    p = projected_points[i]
                    if p is None:
                        points = []
                        break

                    x, y = p
                    points.append(Vector2(x, y))

                if len(points) < 3:
                    continue

                draw_triangle_fan(points, len(points), face.color)
   
def load_object(filename, debug=False) -> Object:
    
    try:
        with open(filename, 'r') as file:
            object_text = file.read()
    except FileNotFoundError:
        print('\033[91m' + f"Error: File '{filename}' not found." + '\033[0m')
    except Exception as error:
        print('\033[91m' + f"Error: '{error}' " + '\033[0m')
        
    print('\033[92m' + f"File: {filename} was loaded succesfully." + '\033[0m')
    obj = Object()
    obj.path = filename
    for line in object_text.splitlines():
        line = line.strip()
        
        if not line or line.startswith("#"):
            continue
        
        parts = line.split()
        if parts[0] == 'v':
            x = -float(parts[1])
            y = -float(parts[2])
            z = float(parts[3])
            vertex = Vertex(x, y, z)
            obj.vertices.append(vertex)
        elif parts[0] == 'f':
            face = Face()
            for part in parts[1:]:
                index = int(part.split('/')[0]) - 1
                face.vertices.append(obj.vertices[index])
                face.face_vertices.append(index)
                value = len(face.vertices)
                
                if value == 3:
                    obj.tri_count += 1
                elif value == 4:
                    obj.quad_count += 1
                elif value > 4:
                    obj.ngon_count += 1
                    
            obj.faces.append(face)
            
    if debug == True:
        print('\033[94m' + f"Loaded object from '{filename}':"  + '\033[0m')
        print('\033[94m' + f"  Vertices count: {len(obj.vertices)}" + '\033[0m')
        print('\033[94m' + "  Vertices:" + '\033[0m')  
        for vertex in obj.vertices:
            print('\033[94m' + f"    ({vertex.x}, {vertex.y}, {vertex.z})" + '\033[0m')
            
        print('\033[94m' + f"  Faces count: {len(obj.faces)}" + '\033[0m')
        print('\033[94m' + f"  Faces indexes: " + '\033[0m')
        for face in obj.faces:
            print('\033[94m' + f"    Face indexes: {face.face_vertices}" + '\033[0m')

    return obj

def draw_object_statistics(object: Object):
    x = 10
    y = 0
    line_height = 20

    lines = [
        f"Object path: {object.path}",
        f"Vertices total: {len(object.vertices)}",
        f"Faces total: {len(object.faces)}",
        f"Tris: {object.tri_count}/{len(object.faces)}",
        f"Quads: {object.quad_count}/{len(object.faces)}",
        f"N-gons: {object.ngon_count}/{len(object.faces)}"
    ]

    for line in lines:
        y = draw_text_offset(line, x, y, line_height, 20, BLACK)
        
def draw_text_offset(text, x, y, line_height, fontsize, color):
    draw_text(text, x, y, fontsize, color)
    return y + line_height
    

