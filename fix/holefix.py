from classes import Vector
from math import acos

class HoleFixer:

    @staticmethod
    def fix(polygons, graph):
        boundary_edges_clusters = HoleFixer.find_boundary_edges(polygons, graph)
        boundary_edges_clusters = HoleFixer.sort_boundary_clusters(boundary_edges_clusters)
        print(boundary_edges_clusters)



    @staticmethod
    def get_angle(point1, vertex, point2):
        side1_square = (point1[0]-vertex[0])**2+(point1[1]-vertex[1])**2+(point1[2]-vertex[2])**2
        side2_square = (vertex[0]-point2[0])**2+(vertex[1]-point2[1])**2+(vertex[2]-point2[2])**2
        back_side_square = (point1[0]-point2[0])**2+(point1[1]-point2[1])**2+(point1[2]-point2[2])**2
        angle_cos = (side1_square+side2_square-back_side_square)/2/(side1_square*side2_square)**0.5
        return acos(angle_cos)


    @staticmethod
    def triangles_intersect(triangle_a, triangle_b):
        return HoleFixer.triangle_includes(triangle_a, triangle_b) or HoleFixer.triangle_includes(triangle_b, triangle_a)

    @staticmethod
    def triangle_includes(triangle_a, triangle_b):
        triangle, points = HoleFixer.project_intersections(triangle_a, triangle_b)
        if not points:
            return False
        x1,y1=triangle[0]
        x2,y2=triangle[1]
        x3,y3=triangle[2]
        vector1=Vector((x2-x1-((x2-x1)*(x3-x2)+(y2-y1)*(y3-y2))*(x3-x2)/((x3-x2)**2+(y3-y2)**2)), (y2-y1-((x2-x1)*(x3-x2)+(y2-y1)*(y3-y2))*(y3-y2)/((x3-x2)**2+(y3-y2)**2)), 0)
        vector2=Vector((x1-x2-((x1-x2)*(x3-x1)+(y1-y2)*(y3-y1))*(x3-x1)/((x3-x1)**2+(y3-y1)**2)), (y1-y2-((x1-x2)*(x3-x1)+(y1-y2)*(y3-y1))*(y3-y1)/((x3-x1)**2+(y3-y1)**2)), 0)
        vector3=Vector((x1-x3-((x1-x3)*(x2-x1)+(y1-y3)*(y2-y1))*(x2-x1)/((x2-x1)**2+(y2-y1)**2)), (y1-y3-((x1-x3)*(x2-x1)+(y1-y3)*(y2-y1))*(y2-y1)/((x2-x1)**2+(y2-y1)**2)), 0)
        
        # hx = x1 - (x1*(x2-x1) + y1*(y2-y1)) * (x2-x1) / ((x2-x1)² + (y2-y1)²)
        # hy = y1 - (x1*(x2-x1) + y1*(y2-y1)) * (y2-y1) / ((x2-x1)² + (y2-y1)²)

        for point in points:
            vector = Vector(point[0], point[1], 0)
            if 0 <= (((vector1)*(vector-Vector(x1,y1,0)))/abs(vector1)) <= abs(vector1) and \
                0 <= (((vector2)*(vector-Vector(x2,y2,0)))/abs(vector2)) <= abs(vector2) and \
                0 <= (((vector3)*(vector-Vector(x3,y3,0)))/abs(vector3)) <= abs(vector3):
                return True
        return False

    
    @staticmethod
    def project_intersections(triangle_a, triangle_b):
        point_0 = Vector(triangle_b[0][0], triangle_b[0][1], triangle_b[0][2])
        point_1 = Vector(triangle_b[1][0], triangle_b[1][1], triangle_b[1][2])
        point_2 = Vector(triangle_b[2][0], triangle_b[2][1], triangle_b[2][2])

        edge1 = point_1 - point_0
        edge2 = point_2 - point_0

        normal = Vector(
            edge1.y * edge2.z - edge1.z * edge2.y,
            edge1.z * edge2.x - edge1.x * edge2.z,
            edge1.x * edge2.y - edge1.y * edge2.x
        )
        normal.normalize()

        basis_u = Vector(edge1.x, edge1.y, edge1.z)
        basis_u.normalize()

        basis_v = Vector(
            normal.y * basis_u.z - normal.z * basis_u.y,
            normal.z * basis_u.x - normal.x * basis_u.z,
            normal.x * basis_u.y - normal.y * basis_u.x
        )
        basis_v.normalize()

        def to_2d(point):
            v = Vector(point[0] - point_0.x, point[1] - point_0.y, point[2] - point_0.z)
            u_coord = v * basis_u
            v_coord = v * basis_v
            return (u_coord, v_coord)

        b_2d = [to_2d(triangle_b[0]), to_2d(triangle_b[1]), to_2d(triangle_b[2])]

        intersections_2d = []

        for i in range(3):
            pa = Vector(triangle_a[i][0], triangle_a[i][1], triangle_a[i][2])
            pb = Vector(triangle_a[(i + 1) % 3][0], triangle_a[(i + 1) % 3][1], triangle_a[(i + 1) % 3][2])

            da = (pa - point_0) * normal
            db = (pb - point_0) * normal

            if da * db < 0 or abs(da) < 1e-12 or abs(db) < 1e-12:
                t = -da / (db - da) if abs(db - da) > 1e-12 else 0.0
                if 0.0 <= t <= 1.0:
                    px = pa.x + t * (pb.x - pa.x)
                    py = pa.y + t * (pb.y - pa.y)
                    pz = pa.z + t * (pb.z - pa.z)
                    intersections_2d.append(to_2d((px, py, pz)))


        return b_2d, intersections_2d

    @staticmethod
    def sort_boundary_clusters(boundary_edges_clusters):
        sorted_clusters = []
        
        for cluster in boundary_edges_clusters:
            if not cluster:
                continue
            
            sorted_cluster = [cluster[0]]
            remaining = cluster[1:].copy()
            
            while remaining:
                last_edge = sorted_cluster[-1]
                last_point = last_edge[1]

                found = False
                for i, edge in enumerate(remaining):
                    point_0, point_1 = edge

                    if point_0 == sorted_cluster[0][0] and point_1 == last_point:
                        sorted_cluster.append((point_1, point_0))
                        remaining.pop(i)
                        found = True
                        sorted_clusters.append(sorted_cluster)
                        if remaining:
                            sorted_cluster = [remaining[0]]
                        break

                    if point_1 == sorted_cluster[0][0] and point_0 == last_point:
                        sorted_cluster.append(edge)
                        remaining.pop(i)
                        found = True
                        sorted_clusters.append(sorted_cluster)
                        if remaining:
                            sorted_cluster = [remaining[0]]
                        break
                    
                    if point_0 == last_point:
                        sorted_cluster.append(edge)
                        remaining.pop(i)
                        found = True
                        break
                    elif point_1 == last_point:
                        sorted_cluster.append((point_1, point_0))
                        remaining.pop(i)
                        found = True
                        break
                    

                if not found:
                    sorted_cluster.extend(remaining)
                    print(f"⚠️ Предупреждение: разрыв цепочки в кластере! Не найдено ребро для точки {last_point}")
                    break
                
            sorted_clusters.append(sorted_cluster)
        
        return sorted_clusters
        
    @staticmethod
    def find_vertex_neighbours(vertex, polygons):
        neighbours = []
        for polygon in polygons:
            point_0, point_1, point_2 = polygon
            if vertex == point_0 or vertex == point_1 or vertex == point_2:
                neighbours.append(polygon)
        return neighbours

    @staticmethod
    def find_boundary_edges(polygons, graph):
        def sort_edge(point_a, point_b):
            if (point_a[0] < point_b[0] or 
                (point_a[0] == point_b[0] and point_a[1] < point_b[1]) or 
                (point_a[0] == point_b[0] and point_a[1] == point_b[1] and point_a[2] < point_b[2])):
                return (point_a, point_b)
            else:
                return (point_b, point_a)
        
        boundary_edges = []
        for polygon, neighbours in graph.items():
            if len(neighbours) <= 2:
                point_0, point_1, point_2 = polygon
                edge_0 = sort_edge(point_0, point_1)
                edge_1 = sort_edge(point_1, point_2)
                edge_2 = sort_edge(point_2, point_0)
                neighbour_edges=[]
                for neighbour in neighbours:
                    neighbour_point_0, neighbour_point_1, neighbour_point_2 = neighbour
                    neighbour_edges.append(sort_edge(neighbour_point_0, neighbour_point_1))
                    neighbour_edges.append(sort_edge(neighbour_point_1, neighbour_point_2))
                    neighbour_edges.append(sort_edge(neighbour_point_2, neighbour_point_0))
                if edge_0 not in neighbour_edges:
                    boundary_edges.append(edge_0)
                if edge_1 not in neighbour_edges:
                    boundary_edges.append(edge_1)
                if edge_2 not in neighbour_edges:
                    boundary_edges.append(edge_2)

        
        edge_graph = {}
        for edge in boundary_edges:
            edge_graph[edge] = []
        
        for i in range(len(boundary_edges)):
            for j in range(i + 1, len(boundary_edges)):
                e1 = boundary_edges[i]
                e2 = boundary_edges[j]
                if e1[0] == e2[0] or e1[0] == e2[1] or e1[1] == e2[0] or e1[1] == e2[1]:
                    edge_graph[e1].append(e2)
                    edge_graph[e2].append(e1)
        
        visited = set()
        clusters = []
        for edge in boundary_edges:
            if edge in visited:
                continue
            
            cluster = []
            queue = [edge]
            visited.add(edge)
            
            while queue:
                current = queue.pop(0)
                cluster.append(current)
                
                for neighbor in edge_graph.get(current, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            clusters.append(cluster)
        
        return clusters

