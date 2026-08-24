from classes import Vector, Point, Face
from file_operations.read import read_file
from render.render import render
import math
from render.get_charset import brightness_sort
from fix.separate import Separator
from fix.holefix import HoleFixer
import time
import os
from file_operations.write import Writer

path = "models"
name = "holetest"

if path[-1] != "/":
    path+="/"

header, polygons, dimensions = read_file(path+name+".stl")



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


parts, graph = Separator.separate(polygons, 0.001)

if sum([len(i) for i in parts]) != len(polygons):
    print(f"получено {len(polygons)} разделено {sum([len(i) for i in parts])} граней")


print(HoleFixer.fix(parts[0], graph)) # временно тест



print("done")
for part_idx in range(len(parts)):
    for face_idx in range(len(parts[part_idx])):
        parts[part_idx][face_idx] = Face(Point(parts[part_idx][face_idx][0][0], parts[part_idx][face_idx][0][1], parts[part_idx][face_idx][0][2]),
                                         Point(parts[part_idx][face_idx][1][0], parts[part_idx][face_idx][1][1], parts[part_idx][face_idx][1][2]),
                                         Point(parts[part_idx][face_idx][2][0], parts[part_idx][face_idx][2][1], parts[part_idx][face_idx][2][2])
                                         )

number=1

if not os.path.exists(path+name):
    os.mkdir(path+name)
    for part_n in range(len(parts)):
        Writer.write(parts[part_n], f"{path}{name}/{name}{str(part_n+1)}.stl", f"{name}{str(part_n+1)}")
else:
    while os.path.exists(path+name+str(number)):
        number+=1
    os.mkdir(path+name+str(number))
    for part_n in range(len(parts)):
        Writer.write(parts[part_n], f"{path}{name}{str(number)}/{name}{str(part_n+1)}.stl", f"{name}{str(part_n+1)}")






