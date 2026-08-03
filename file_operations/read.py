import struct
import time

from classes import Point, Vector, Face


def triangle_read(bytes_400):
    points=[point_read(bytes_400[12*i:12*(i+1)]) for i in range(4)]
    vector=Vector(points[0][0], points[0][1], points[0][2])
    point1=Point(points[1][0], points[1][1], points[1][2])
    point2=Point(points[2][0], points[2][1], points[2][2])
    point3=Point(points[3][0], points[3][1], points[3][2])
    return (Face(point1, point2, point3, vector), (min(points[1][0],points[2][0],points[3][0]), min(points[1][1],points[2][1],points[3][1]), min(points[1][2],points[2][2],points[3][2]), max(points[1][0],points[2][0],points[3][0]), max(points[1][1],points[2][1],points[3][1]), max(points[1][2],points[2][2],points[3][2])))



def point_read(bytes_96):
    x=real_32_read(bytes_96[:4])
    y=real_32_read(bytes_96[4:8])
    z=real_32_read(bytes_96[8:12])
    return (x,y,z)

def real_32_read(real_32):
    real32_number = struct.unpack('<f', bytes(int(x, 16) for x in real_32))[0]
    return real32_number




def read_file(path):
    with open(path, "rb") as file:
        raw=file.read()
    
    result = [f"{b:02x}" for b in raw]

    header = result[:80]


    number_of_triangles_32 = result[80:84]

    number_of_triangles = sum([int(number_of_triangles_32[i], 16)*256**i for i in range(4)])

    print(number_of_triangles)

    result=result[84:]


    triangles=[]

    x_min=None
    x_max=None
    y_min=None
    y_max=None
    z_min=None
    z_max=None

    for i in range(number_of_triangles):
        face, measures = triangle_read(result[50*i:50*(i+1)])
        triangles.append(face)
        if x_min:
            if measures[0] < x_min:
                x_min=measures[0]
        else:
            x_min=measures[0]
        if y_min:
            if measures[1] < y_min:
                y_min=measures[1]
        else:
            y_min=measures[1]
        if z_min:
            if measures[2] < z_min:
                z_min=measures[2]
        else:
            z_min=measures[2]
        if x_max:
            if measures[3] > x_max:
                x_max=measures[3]
        else:
            x_max=measures[3]
        if y_max:
            if measures[4] > y_max:
                y_max=measures[4]
        else:
            y_max=measures[4]
        if z_max:
            if measures[5] > z_max:
                z_max=measures[5]
        else:
            z_max=measures[5]


    return (header, triangles, (x_min,x_max,y_min,y_max,z_min,z_max))

