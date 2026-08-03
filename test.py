import struct

class Point:

    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    

class Vector:

    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z
    
    def __str__(self):
        return "{"+f"{self.x}, {self.y}, {self.z}"+"}"

class Face:

    def __init__(self, p1, p2, p3, normal=Vector(0,0,0)):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.normal = normal

    def __str__(self):
        return f"[{str(self.p1)} {str(self.p2)} {str(self.p3)}]"

    def __repr__(self):
        return f"[{str(self.p1)} {str(self.p2)} {str(self.p3)}]"



def triangle_read(bytes_400):
    points=[point_read(bytes_400[12*i:12*(i+1)]) for i in range(4)]
    vector=Vector(points[0][0], points[0][1], points[0][2])
    point1=Point(points[1][0], points[1][1], points[1][2])
    point2=Point(points[2][0], points[2][1], points[2][2])
    point3=Point(points[3][0], points[3][1], points[3][2])
    return Face(point1, point2, point3, vector)



def point_read(bytes_96):
    x=real_32_read(bytes_96[:4])
    y=real_32_read(bytes_96[4:8])
    z=real_32_read(bytes_96[8:12])
    return (x,y,z)

def real_32_read(real_32):
    real32_number = struct.unpack('<f', bytes(int(x, 16) for x in real_32))[0]
    return real32_number









with open("tetrahedron0.stl", "rb") as file:
# with open("octahedron0.stl", "rb") as file:
    raw=file.read()

result = [f"{b:02x}" for b in raw]


header = result[:80]


number_of_triangles_32 = result[80:84]

number_of_triangles = sum([int(number_of_triangles_32[i], 16)*256**i for i in range(4)])

result=result[84:]


triangles=[]

for i in range(number_of_triangles):
    triangles.append(triangle_read(result[:50]))
    result=result[50:]

for i in triangles:
    print(i)

