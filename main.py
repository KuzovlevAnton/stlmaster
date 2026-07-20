from classes import Vector, Point, Face
from read import read_file
from render import render
import math
from get_charset import brightness_sort
from separate import Separator
import time
import os
from write import Writer

name = "separatetest"

header, polygons, dimensions = read_file(name+".stl")



center = Point(
    (dimensions[0]+dimensions[1])/2,
    (dimensions[2]+dimensions[3])/2,
    (dimensions[4]+dimensions[5])/2
        )
diagonal = ((dimensions[0]-dimensions[1])**2+(dimensions[2]-dimensions[3])**2+(dimensions[4]-dimensions[5])**2)**0.5

# print(center, diagonal)


# camera = Vector(1,1,1).normalize()
# os.system("clear")
# for angle in range(0, 3600, 1):
#     render(polygons, diagonal, center, 100, 80, camera=Vector(camera.x*math.cos(math.radians(angle))-camera.y*math.sin(math.radians(angle)), camera.x*math.sin(math.radians(angle))+camera.y*math.cos(math.radians(angle)), camera.z), chars=brightness_sort())
#     time.sleep(0.01)


parts=Separator.separate(polygons, 0.001)

if sum([len(i) for i in parts]) != len(polygons):
    print(f"получено {len(polygons)} разделено {sum([len(i) for i in parts])} граней")

print("done")
for part_idx in range(len(parts)):
    for face_idx in range(len(parts[part_idx])):
        parts[part_idx][face_idx] = Face(Point(parts[part_idx][face_idx][0][0], parts[part_idx][face_idx][0][1], parts[part_idx][face_idx][0][2]),
                                         Point(parts[part_idx][face_idx][1][0], parts[part_idx][face_idx][1][1], parts[part_idx][face_idx][1][2]),
                                         Point(parts[part_idx][face_idx][2][0], parts[part_idx][face_idx][2][1], parts[part_idx][face_idx][2][2])
                                         )


os.mkdir(name)
for part_n in range(len(parts)):
    Writer.write(parts[part_n], f"{name}/{name}{str(part_n+1)}.stl", f"{name}{str(part_n+1)}")
