from classes import Vector, Point
from read import read_file
from render import render
import math
from get_charset import brightness_sort
from separate import Separator
import time
import os

# header, polygons, dimensions = read_file("octahedron0.stl")
# header, polygons, dimensions = read_file("tetrahedron0.stl")
# header, polygons, dimensions = read_file("cube.stl")
# header, polygons, dimensions = read_file("flashlight73.stl")
header, polygons, dimensions = read_file("_ОСНОВА ШУСТРИК3 ФУТБОЛ 20042026 (1).stl")
# header, polygons, dimensions = read_file("sphere.stl")
# header, polygons, dimensions = read_file("separatetest.stl")



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


Separator.separate(polygons, 0.001)
