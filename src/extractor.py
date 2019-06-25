#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from filereader3db import *
from obj_generator import *


def default_output_name():
    temp = sys.argv[1].split(".")
    temp[-1] = "obj"
    return ".".join(temp)


def print_help():
    print("Usage:")
    print("python extractor.py path/to/file [options]")
    print("Options:")
    print("    -o <file>                           Output file name")
    print("    -s <floating point value>           Scale of the model")
    exit(1)


if __name__ == '__main__':

    scale = 1
    output_filename = ""

    if len(sys.argv) < 2 or len(sys.argv) > 6:
        print("Invalid number of arguments!")
        print_help()
    elif len(sys.argv) == 2:
        output_filename = default_output_name()
    elif len(sys.argv) == 4:
        options = {sys.argv[2][1:]: sys.argv[3]}
        if "o" in options.keys():
            output_filename = options["o"]
        elif "s" in options.keys():
            try:
                scale = float(options["s"])
            except:
                print(f"Invalid scale value: {options['s']}")
                print_help()
            output_filename = default_output_name()
        else:
            print("Invalid parameter!")
            print_help()
    elif len(sys.argv) == 6:
        options = {sys.argv[2][1:]: sys.argv[3], sys.argv[4][1:]: sys.argv[5]}
        if "o" in options.keys():
            output_filename = options["o"]
        else:
            print("Invalid parameter!")
            print_help()
        if "s" in options.keys():
            try:
                scale = float(options["s"])
            except:
                print(f"Invalid scale value: {options['s']}")
                print_help()
        else:
            print("Invalid parameter!")
            print_help()

    filename = sys.argv[1]

    g = Graph()
    a = UtfFile()

    modeldata = a.load_utf_file(filename)
    #print(get_as_string(modeldata["\\"]["Exporter Version"]['value']))

    print()

    data = get_as_float_list(modeldata['\\']['openFLAME 3D N-mesh']['Vertices']['Object vertex list']['value'])
    for i in range(0, len(data), 3):
        g.add_vertex(Vertex(float(data[i]), float(data[i + 2]), float(data[i + 1]), scale))

    data = get_as_int_list(modeldata['\\']['openFLAME 3D N-mesh']['Edges']['Vertex list']['value'])
    for i in range(0, len(data), 2):
        g.add_edge(Edge(int(data[i]), int(data[i + 1])))

    g.get_all_vertices()
    g.generate_triangles()
    g.fix_ordering(False)
    g.generate_polygons_for_obj(output_filename, True)

    print("Done")



