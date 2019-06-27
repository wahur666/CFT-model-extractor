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

    def get_formatted_vertex_list(self):
        return f"{format(self.x, 'f')} {format(self.y, 'f')} {format(self.z, 'f')} "

    def __str__(self):
        return f"Vertex X={self.x} Y={self.y} Z={self.z}"

    def __repr__(self):
        return f"Vertex X={self.x} Y={self.y} Z={self.z}"


class TextureCoords:

    def __init__(self, u, v):
        self.u = u
        self.v = v

    def get_formatted_texture_coord_list(self):
        return f"{format(self.u, 'f')} {format(self.v, 'f')}"

    def __str__(self):
        return f"TextureCoord U={self.u} V={self.v}"

    def __repr__(self):
        return f"TextureCoord U={self.u} V={self.v}"


class ObjModel:

    def __init__(self, model):
        self.model = model
        self.vertices = []
        self.face_groups = []
        self.face_group_surface_normals = []
        self.surface_normals = []
        self.vertex_batch_list = []
        self.texture_coord_list = []
        self.vertex_normals = []
        self.texture_batch_list = []

    def export_to_obj(self, path, scale=1):
        mesh = self.model['\\']['openFLAME 3D N-mesh']

        self.create_vertices(mesh)

        self.create_face_groups(mesh)

        self.create_normals(mesh)

        self.create_texture_coordinates(mesh)

        self.vertex_batch_list = get_as_int_list(mesh['Vertices']['Vertex batch list']['value'])

        with open(path, "w") as outfile:
            for vertex in self.vertices:
                vertex.scale_vertex(scale)
                s = "v " + vertex.get_formatted_vertex_list()
                outfile.write(s + "\n")

            outfile.write(f"#{len(self.vertices)} Vertices \n\n")

            for texture_coord in self.texture_coord_list:
                s = "vt " + texture_coord.get_formatted_texture_coord_list()
                outfile.write(s + "\n")
            outfile.write(f"#{len(self.texture_coord_list)} Texture Coordinates \n\n")

            for vertex in self.surface_normals:
                s = "vn " + vertex.get_formatted_vertex_list()
                outfile.write(s + "\n")

            outfile.write(f"#{len(self.surface_normals)} Normals \n\n")



            triangles = 0
            for face_group_index in range(len(self.face_groups)):
                face_group = self.face_groups[face_group_index]
                for i, index in enumerate(range(0, len(face_group), 3)):
                    vertex_1 = self.vertex_batch_list[face_group[index]] + 1
                    vertex_2 = self.vertex_batch_list[face_group[index + 1]] + 1
                    vertex_3 = self.vertex_batch_list[face_group[index + 2]] + 1
                    uv_1 = self.texture_batch_list[face_group[index]] + 1
                    uv_2 = self.texture_batch_list[face_group[index + 1]] + 1
                    uv_3 = self.texture_batch_list[face_group[index + 2]] + 1
                    normal_1 = self.vertex_normals[vertex_1 - 1] + 1
                    normal_2 = self.vertex_normals[vertex_2 - 1] + 1
                    normal_3 = self.vertex_normals[vertex_3 - 1] + 1
                    outfile.write(f"f {vertex_1}/{uv_1}/{normal_1} {vertex_2}/{uv_2}/{normal_2} {vertex_3}/{uv_3}/{normal_3} \n")
                    triangles += 1

            outfile.write("#%d Faces" % triangles)

    def create_normals(self, mesh):
        data = get_as_float_list(mesh['Normals']['Surface normal list']['value'])
        for i in range(0, len(data), 3):
            self.surface_normals.append(Vertex(float(data[i]), float(data[i + 1]), float(data[i + 2])))
        self.vertex_normals = get_as_int_list(mesh['Vertices']['Vertex normal']['value'])

    def create_face_groups(self, mesh):
        face_group_count = get_as_int_list(mesh['Face groups']['Count']['value'])[0]
        for i in range(face_group_count):
            face_group = mesh['Face groups'][f'Group{i}']
            self.face_groups.append(get_as_int_list(face_group['Face vertex chain']['value']))
            self.face_group_surface_normals.append(get_as_int_list(face_group['Face normal']['value']))

    def create_vertices(self, mesh):
        data = get_as_float_list(mesh['Vertices']['Object vertex list']['value'])
        for i in range(0, len(data), 3):
            self.vertices.append(Vertex(float(data[i]), float(data[i + 1]), float(data[i + 2])))
        self.texture_batch_list = get_as_int_list(mesh['Vertices']['Texture batch list']['value'])

    def create_texture_coordinates(self, mesh):
        data = get_as_float_list(mesh['Vertices']['Texture vertex list']['value'])
        for i in range(0, len(data), 2):
            self.texture_coord_list.append(TextureCoords(float(data[i]), float(data[i + 1])))
