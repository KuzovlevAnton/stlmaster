import struct

class Writer:

    @staticmethod
    def write(polygons, path, header):
        with open(path, "wb") as file:
            header_bytes = header.encode('ascii').ljust(80, b'\x00')[:80]
            file.write(header_bytes)
            
            num_triangles = len(polygons)
            file.write(struct.pack('<I', num_triangles))

            for polygon in polygons:
                Writer.write_polygon(file, polygon)
    
    @staticmethod
    def write_polygon(file, polygon):
        file.write(struct.pack('<fff', 0.0, 0.0, 0.0)) # добавить просчёт нормали в классе
        
        file.write(struct.pack('<fff', polygon.p1.x, polygon.p1.y, polygon.p1.z))
        file.write(struct.pack('<fff', polygon.p2.x, polygon.p2.y, polygon.p2.z))
        file.write(struct.pack('<fff', polygon.p3.x, polygon.p3.y, polygon.p3.z))
        
        file.write(struct.pack('<H', 0))
