#!/usr/bin/python
# -*- coding: utf-8 -*-
from filereader3db import *


class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def scale_vertex(self, scale):
        self.x *= scale
        self.y *= scale
        self.z *= scale

    def get_vertex_list(self, flip_xy=False):
        return [str(self.x), str(self.y), str(self.z)] if not flip_xy else [str(self.x), str(self.z), str(self.y)]

    def __str__(self):
        return "Vertex X=%g Y=%g Z=%g" % (self.x, self.y, self.z)

    def __repr__(self):
        return "Vertex[X=%g,Y=%g,Z=%g]" % (self.x, self.y, self.z)


class ObjModel:

    def __init__(self, model):
        self.model = model
        self.vertices = []
        self.face_groups = []
        self.face_group_surface_normals = []
        self.surface_normals = []
        self.vertex_batch_list = []

    def export_to_obj(self, path, scale=1):
        mesh = self.model['\\']['openFLAME 3D N-mesh']
        data = get_as_float_list(mesh['Vertices']['Object vertex list']['value'])
        for i in range(0, len(data), 3):
            self.vertices.append(Vertex(float(data[i]), float(data[i + 1]), float(data[i + 2])))

        face_group_count = get_as_int_list(mesh['Face groups']['Count']['value'])[0]

        for i in range(face_group_count):
            face_group = mesh['Face groups'][f'Group{i}']
            self.face_groups.append(get_as_int_list(face_group['Face vertex chain']['value']))
            self.face_group_surface_normals.append(get_as_int_list(face_group['Face normal']['value']))

        data = get_as_float_list(mesh['Normals']['Surface normal list']['value'])
        for i in range(0, len(data), 3):
            self.surface_normals.append(Vertex(float(data[i]), float(data[i + 1]), float(data[i + 2])))

        self.vertex_batch_list = get_as_int_list(mesh['Vertices']['Vertex batch list']['value'])

        with open(path, "w") as outfile:
            for vertex in self.vertices:
                vertex.scale_vertex(scale)
                s = "v " + " ".join(vertex.get_vertex_list())
                outfile.write(s + "\n")

            outfile.write("#%d Vertexes \n\n" % len(self.vertices))

            triangles = 0
            for face_group in self.face_groups:
                for index in range(0, len(face_group), 3):
                    outfile.write("f %d %d %d \n" % (self.vertex_batch_list[face_group[index]] + 1, self.vertex_batch_list[face_group[index + 1]] + 1, self.vertex_batch_list[face_group[index + 2]] + 1))
                    triangles += 1

            outfile.write("#%d Faces" % triangles)




def create_vertices(model: Dict, scale=1):
    vertices  = []