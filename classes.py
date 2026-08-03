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
    
    def normalize(self):
        length=(self.x**2+self.y**2+self.z**2)**0.5
        self.x/=length
        self.y/=length
        self.z/=length
        return self
    
    def multiply(self, k):
        self.x*=k
        self.y*=k
        self.z*=k
        return self

    def __abs__(self):
        return (self.x**2+self.y**2+self.z**2)**0.5

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y, self.z-other.z)
    
    def __mul__(self, other):
        return self.x*other.x+self.y*other.y+self.z*other.z
    
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

# add normal normalize