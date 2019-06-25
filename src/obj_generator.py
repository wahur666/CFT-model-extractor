#!/usr/bin/python
# -*- coding: utf-8 -*-


class Vertex:
    def __init__(self, x, y, z, scale=1):
        self.x = x * scale
        self.y = y * scale
        self.z = z * scale

    def get_vertex_list(self, flip_xy=False):
        return [str(self.x), str(self.y), str(self.z)] if not flip_xy else [str(self.x), str(self.z), str(self.y)]

    def __str__(self):
        return "Vertex X=%g Y=%g Z=%g" % (self.x, self.y, self.z)

    def __repr__(self):
        return "Vertex[X=%g,Y=%g,Z=%g]" % (self.x, self.y, self.z)


class Edge:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def __repr__(self):
        return "Edge[P1=%d,P2=%d]" % (self.point1, self.point2)

    def __contains__(self, item):
        return item == self.point1 or item == self.point2

    def get_the_other_vertex(self, vertex):
        if vertex == self.point1:
            return self.point2
        else:
            return self.point1

    def has(self, vertex):
        return vertex == self.point1 or vertex == self.point2

    def __eq__(self, other):
        return {self.point1, self.point2} == {other.point1, other.point2}

    def __cmp__(self, other):
        return self.point1 < other.point1

    def get_points(self):
        return self.point1, self.point2


class Triangle:
    def __init__(self, vertex1, vertex2, vertex3):
        self.vertexes = [vertex1, vertex2, vertex3]
        self.vertexes.sort()

    def __eq__(self, other):
        return set(self.vertexes) == set(other.vertexes)

    def __hash__(self):
        return hash(tuple(sorted(set(self.vertexes))))

    def __repr__(self):
        return "Triangle[V1=%d,V2=%d,V3=%d]" % (self.vertexes[0], self.vertexes[1], self.vertexes[2])

    def __lt__(self, other):
        for i in range(len(self.vertexes)):
            if self.vertexes[i] != other.vertexes[i]:
                return self.vertexes[i] < other.vertexes[i]

    def reverse_vertex_ordering(self):
        self.vertexes[1], self.vertexes[2] = self.vertexes[2], self.vertexes[1]

    def shift_vertexes(self):
        self.vertexes.append(self.vertexes.pop(0))

    def has_common_edge(self, other):
        return len(set(self.vertexes) & set(other.vertexes)) == 2

    def get_common_edge(self, other):
        return sorted(list(set(self.vertexes) & set(other.vertexes)))

    def rotate_to(self, num):
        while self.vertexes[0] != num:
            self.shift_vertexes()

    def is_the_order_correct_to(self, other):
        mini = self.get_common_edge(other)[0]
        self.rotate_to(mini)
        other.rotate_to(mini)
        return self.vertexes[1] == other.vertexes[2] or self.vertexes[2] == other.vertexes[1]


class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = []
        self.vertex_index = 0
        self.found_vertexes = []
        self.triangles = set()

    def add_vertex(self, vertex):
        self.vertices[self.vertex_index] = vertex
        self.vertex_index += 1

    def add_edge(self, edge):
        if edge.point1 in self.vertices.keys():
            if edge.point2 in self.vertices.keys():
                self.edges.append(edge)
            else:
                print("Cant add edge, there is no vertex with index: {}", edge.point2)
        else:
            print("Cant add edge, there is no vertex with index: {}", edge.point1)

    def find_sub_graphs(self, root=0):
        self.found_vertexes = []
        done_vertexes = set()
        process_queue = list()

        process_queue.append(root)
        done_vertexes.add(root)
        while process_queue:
            current = process_queue.pop(0)

            # Here you process the Vertex
            self.found_vertexes.append(current)

            for item in self.adjacent_points(current):
                if item not in done_vertexes:
                    done_vertexes.add(item)
                    process_queue.append(item)

    def get_all_vertices(self):
        self.found_vertexes = [key for key, value in self.vertices.items()]

    def generate_triangles(self):
        for item in self.found_vertexes:
            for adj1 in self.adjacent_points(item):
                first_set = set(self.adjacent_points(item))
                second_set = set(self.adjacent_points(adj1))
                intersected_points = list(first_set & second_set)
                for point in intersected_points:
                    if Triangle(item, adj1, point) not in self.triangles:
                        self.triangles.add(Triangle(item, adj1, point))

    def generate_polygons_for_obj(self, file, flipYZ=False):
        with open(file, "w") as outfile:
            for key, value in self.vertices.items():
                s = "v " + " ".join(value.get_vertex_list(flipYZ))
                outfile.write(s + "\n")

            outfile.write("#%d Vertexes \n\n" % len(self.vertices))

            for item in self.triangles:
                outfile.write("f %d %d %d \n" % (item.vertexes[0] + 1, item.vertexes[1] + 1, item.vertexes[2] + 1))

            outfile.write("#%d Faces" % len(self.triangles))

    def adjacent_points(self, vertex):
        points = []
        for edge in self.edges:
            if vertex in edge:
                points.append(edge.get_the_other_vertex(vertex))
        return points

    def adjacent_triangles(self, triangle):
        triangles = []
        for item in self.triangles:
            if item.has_common_edge(triangle):
                triangles.append(item)
        return triangles

    def fix_ordering(self, revese=False):
        '''
        :param revese: reverse the first triangle points ordering
        '''
        all_item = set()
        while self.triangles:
            self.triangles = sorted(list(self.triangles))
            main_triangle = self.triangles.pop(0)
            if revese:
                main_triangle.reverse_vertex_ordering()

            done_triangles = set()
            process_queue = list()

            process_queue.append(main_triangle)
            done_triangles.add(main_triangle)

            while process_queue:
                current = process_queue.pop(0)

                adjje = self.adjacent_triangles(current)

                for item in adjje:
                    if item not in done_triangles:
                        # Here you process the Triangle
                        # Check if the triangle points in the right order
                        if not item.is_the_order_correct_to(current):
                            # if not revers the order
                            item.reverse_vertex_ordering()
                        done_triangles.add(item)
                        process_queue.append(item)
                        # self.triangles.remove(item)
            self.triangles = set(self.triangles) - done_triangles
            all_item |= done_triangles
        self.triangles = all_item

    def reverse_triangles(self):
        for triangle in self.triangles:
            triangle.reverse_vertex_ordering()