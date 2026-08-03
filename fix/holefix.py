class HoleFixer:

    @staticmethod
    def fix(polygons, graph):
        boundary_edges_clusters = HoleFixer.find_boundary_edges(polygons, graph)
        for i in boundary_edges_clusters:
            print(i)
        return boundary_edges_clusters

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


