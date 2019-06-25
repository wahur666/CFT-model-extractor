#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from filereader3db import *
from obj_generator import *


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Not enough arguments!")
        print("Usage:")
        print("    python app.py path/to/file <output-filename>")
        exit(1)
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        temp = sys.argv[1].split(".")
        temp[-1] = "obj"
        output_filename = ".".join(temp)
    elif len(sys.argv > 2):
        filename = sys.argv[1]
        output_filename = sys.argv[2]

    g = Graph()
    a = UtfFile()

    modeldata = a.load_utf_file(filename)
    #print(get_as_string(modeldata["\\"]["Exporter Version"]['value']))

    print()

    data = get_as_float_list(modeldata['\\']['openFLAME 3D N-mesh']['Vertices']['Object vertex list']['value'])
    for i in range(0, len(data), 3):
        g.add_vertex(Vertex(float(data[i]), float(data[i + 2]), float(data[i + 1])))

    data = get_as_int_list(modeldata['\\']['openFLAME 3D N-mesh']['Edges']['Vertex list']['value'])
    for i in range(0, len(data), 2):
        g.add_edge(Edge(int(data[i]), int(data[i + 1])))

    g.get_all_vertices()
    g.generate_triangles()
    g.fix_ordering(False)
    g.generate_polygons_for_obj(output_filename, True)

    print("Done")



