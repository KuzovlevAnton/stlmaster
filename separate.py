

class Separator:


    @staticmethod
    def separate(polygons, accuracy):
        ids, ids_polygons = Separator.weld(polygons, accuracy)
        # ids_edges=Separator.get_edges(ids_polygons)
        graph=Separator.graph_build(ids_polygons)

        parts=[]
        while ids_polygons:
            part, ids_polygons = Separator.bfs(ids_polygons, graph)
            parts.append(part)
        

        parts = Separator.numerize(parts, ids)

        return parts

    

    @staticmethod
    def weld(polygons, accuracy):
        point_to_id = {}
        ids = {}
        next_id = 0
        ids_polygons = []
        
        def get_point_id(x, y, z):
            nonlocal next_id
            
            scale = int(1 / accuracy)
            key = (round(x * scale) / scale,
                round(y * scale) / scale,
                round(z * scale) / scale)
            
            if key in point_to_id:
                return point_to_id[key]
            
            point_to_id[key] = next_id
            ids[next_id] = key
            new_id = next_id
            next_id += 1
            return new_id
        
        for polygon in polygons:
            id1 = get_point_id(polygon.p1.x, polygon.p1.y, polygon.p1.z)
            id2 = get_point_id(polygon.p2.x, polygon.p2.y, polygon.p2.z)
            id3 = get_point_id(polygon.p3.x, polygon.p3.y, polygon.p3.z)
            
            ids_polygons.append([id1, id2, id3])
    
        return ids, ids_polygons


    @staticmethod
    def get_edges(ids_polygons):
        ids_edges = set()
        for polygon in ids_polygons:
            v0, v1, v2 = polygon

            if v0 < v1:
                edge = (v0, v1)
            else:
                edge = (v1, v0)
            ids_edges.add(edge)

            if v1 < v2:
                edge = (v1, v2)
            else:
                edge = (v2, v1)
            ids_edges.add(edge)

            if v2 < v0:
                edge = (v2, v0)
            else:
                edge = (v0, v2)
            ids_edges.add(edge)
        
        return list(ids_edges)

    @staticmethod
    def graph_build(ids_polygons):
        edge_to_polygons = {}

        def get_edge(point_a, point_b, polygon):
            edge = (point_a, point_b) if point_a < point_b else (point_b, point_a)
            if edge not in edge_to_polygons:
                edge_to_polygons[edge] = []
            edge_to_polygons[edge].append(polygon)
        
        for polygon in ids_polygons:
            point_1, point_2, point_3 = polygon
            
            get_edge(point_1, point_2, polygon)
            get_edge(point_2, point_3, polygon)
            get_edge(point_1, point_3, polygon)
            
        
        graph_dict = {}
        
        for polygons in edge_to_polygons.values():
            for idx1 in range(len(polygons)):
                for idx2 in range(idx1 + 1, len(polygons)):
                    t1 = tuple(polygons[idx1])
                    t2 = tuple(polygons[idx2])
                    
                    if t1 not in graph_dict:
                        graph_dict[t1] = []
                    if t2 not in graph_dict:
                        graph_dict[t2] = []
                    
                    if t2 not in graph_dict[t1]:
                        graph_dict[t1].append(t2)
                    if t1 not in graph_dict[t2]:
                        graph_dict[t2].append(t1)
        return graph_dict
    

    @staticmethod
    def bfs(polygons, graph):
        visited = []
        current = [tuple(polygons.pop(0))]
        neighbours=[]
        while current:
            for current_polygon in current:
                for polygon in graph.get(current_polygon):
                    if polygon not in visited and polygon not in current and polygon not in neighbours:
                        neighbours.append(polygon)
                visited.append(current_polygon)
                if list(current_polygon) in polygons:
                    polygons.remove(list(current_polygon))
            current=neighbours
            neighbours=[]


        return visited, polygons

    def numerize(parts, ids):
        parts_numerized=[]
    
        for part in parts:
            numerized_part = []
            for polygon in part:
                numerized_polygon = (ids[polygon[0]],ids[polygon[1]],ids[polygon[2]])
                numerized_part.append(numerized_polygon)
            parts_numerized.append(numerized_part)
    

        return parts_numerized