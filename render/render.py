from classes import Vector, Point
import matplotlib.pyplot as plt
import cv2, numpy
import sys

def render(polygons, d, c, width=100, height=80, camera=Vector(1,1,1), chars=()):
    # plt.cla()


    def draw_triangle(x1,y1,z1,x2,y2,z2,x3,y3,z3):
        nonlocal screen_chars, screen_depth, width, height, camera, d

        if ((x2-x1)*(y3-y1)-(x3-x1)*(y2-y1)) and ((x2-x1)*(y3-y1)-(x3-x1)*(y2-y1)):
            normal = Vector((y2-y1)*(z3-z1)-(z2-z1)*(y3-y1), (z2-z1)*(x3-x1)-(x2-x1)*(z3-z1), (x2-x1)*(y3-y1)-(y2-y1)*(x3-x1))
            normal.normalize()

            brightness = abs(normal*Vector(0, 0, 1))

            x_z_factor = ((z2-z1)*(y3-y1)-(z3-z1)*(y2-y1))/((x2-x1)*(y3-y1)-(x3-x1)*(y2-y1))
            y_z_factor = ((x2-x1)*(z3-z1)-(x3-x1)*(z2-z1))/((x2-x1)*(y3-y1)-(x3-x1)*(y2-y1))
            z_addition_factor = z1-x_z_factor*x1-y_z_factor*y1

            vector1=Vector((x2-x1-((x2-x1)*(x3-x2)+(y2-y1)*(y3-y2))*(x3-x2)/((x3-x2)**2+(y3-y2)**2)), (y2-y1-((x2-x1)*(x3-x2)+(y2-y1)*(y3-y2))*(y3-y2)/((x3-x2)**2+(y3-y2)**2)), 0)
            vector2=Vector((x1-x2-((x1-x2)*(x3-x1)+(y1-y2)*(y3-y1))*(x3-x1)/((x3-x1)**2+(y3-y1)**2)), (y1-y2-((x1-x2)*(x3-x1)+(y1-y2)*(y3-y1))*(y3-y1)/((x3-x1)**2+(y3-y1)**2)), 0)
            vector3=Vector((x1-x3-((x1-x3)*(x2-x1)+(y1-y3)*(y2-y1))*(x2-x1)/((x2-x1)**2+(y2-y1)**2)), (y1-y3-((x1-x3)*(x2-x1)+(y1-y3)*(y2-y1))*(y2-y1)/((x2-x1)**2+(y2-y1)**2)), 0)
            
            # hx = x1 - (x1*(x2-x1) + y1*(y2-y1)) * (x2-x1) / ((x2-x1)² + (y2-y1)²)
            # hy = y1 - (x1*(x2-x1) + y1*(y2-y1)) * (y2-y1) / ((x2-x1)² + (y2-y1)²)


            kx_relative = 1/(d*width/min(width, height))
            ky_relative = 1/(d*height/min(width, height))


            if abs(vector1) != 0 and abs(vector2) != 0 and abs(vector3) != 0:
                for y in range(int(min(y1,y2,y3)*ky_relative*height), int(max(y1,y2,y3)*ky_relative*height)+1):
                    for x in range(int(min(x1,x2,x3)*kx_relative*width), int(max(x1,x2,x3)*kx_relative*width)+1):
                        vector=Vector(x/(kx_relative*width), y/(ky_relative*height), 0)
                        if 0 <= (((vector1)*(vector-Vector(x1,y1,0)))/abs(vector1)) <= abs(vector1) and \
                            0 <= (((vector2)*(vector-Vector(x2,y2,0)))/abs(vector2)) <= abs(vector2) and \
                            0 <= (((vector3)*(vector-Vector(x3,y3,0)))/abs(vector3)) <= abs(vector3):
                            depth = x_z_factor*x/(kx_relative*width)+y_z_factor*y/(ky_relative*height)+z_addition_factor
                            if depth > screen_depth[height//2+y][width//2+x]:
                                screen_chars[height//2+y][width//2+x]=brightness
                                screen_depth[height//2+y][width//2+x]=depth

        
    def closest_char(brightness, brightness_scheme, symbols):
        if brightness >= max(brightness_scheme):
            return symbols[-1]
        if brightness <= min(brightness_scheme):
            return symbols[0]
        i=0
        while brightness>brightness_scheme[i]:
            i+=1
        if abs(brightness-brightness_scheme[i]) < abs(brightness-brightness_scheme[i-1]):
            return symbols[i]
        else:
            return symbols[i-1]
    
    horizontal = Vector(1,-camera.x/camera.y,0)
    horizontal.multiply(int(camera.y//abs(camera.y)))
    vertical = Vector(-camera.x/(camera.x**2+camera.y**2), -camera.y/(camera.x**2+camera.y**2), 1/camera.z)
    vertical.multiply(-int(camera.z//abs(camera.z)))
    camera.normalize()
    horizontal.normalize()
    vertical.normalize()


    screen_chars=[[0 for _ in range(width)] for _ in range(height)]
    screen_depth=[[-d for _ in range(width)] for _ in range(height)]

    for polygon in polygons:
    # polygon=polygons[0]

        p1x=horizontal*Vector(polygon.p1.x-c.x, polygon.p1.y-c.y, polygon.p1.z-c.z)
        p2x=horizontal*Vector(polygon.p2.x-c.x, polygon.p2.y-c.y, polygon.p2.z-c.z)
        p3x=horizontal*Vector(polygon.p3.x-c.x, polygon.p3.y-c.y, polygon.p3.z-c.z)
        p1y=vertical*Vector(polygon.p1.x-c.x, polygon.p1.y-c.y, polygon.p1.z-c.z)
        p2y=vertical*Vector(polygon.p2.x-c.x, polygon.p2.y-c.y, polygon.p2.z-c.z)
        p3y=vertical*Vector(polygon.p3.x-c.x, polygon.p3.y-c.y, polygon.p3.z-c.z)
        p1z=camera*Vector(polygon.p1.x-c.x, polygon.p1.y-c.y, polygon.p1.z-c.z)
        p2z=camera*Vector(polygon.p2.x-c.x, polygon.p2.y-c.y, polygon.p2.z-c.z)
        p3z=camera*Vector(polygon.p3.x-c.x, polygon.p3.y-c.y, polygon.p3.z-c.z)
        # plt.scatter(p1x, p1y, s=10*(d+p1z)/d, c='red')
        # plt.scatter(p2x, p2y, s=10*(d+p2z)/d, c='red')
        # plt.scatter(p3x, p3y, s=10*(d+p3z)/d, c='red')
        # plt.scatter(d*width/min(width, height)/2, d*height/min(width, height)/2, s=10, c='red')
        # plt.scatter(-d*width/min(width, height)/2, -d*height/min(width, height)/2, s=10, c='red')
        draw_triangle(p1x, p1y, p1z, p2x, p2y, p2z, p3x, p3y, p3z)
        
    

    if not len(chars):
        cv2.imwrite("result.png", numpy.array(screen_chars)*255)
    else:
        
        string=""
        for col in screen_chars:
            for pixel in col:
                string += closest_char(pixel, chars[0], chars[1])
            string+="\n"
    
    sys.stdout.write('\033[H')
    sys.stdout.write(string)
    sys.stdout.flush()

    # plt.show()
    # plt.pause(0.001)
