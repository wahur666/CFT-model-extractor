#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
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

    a = UtfFile()
    model_data = a.load_utf_file(filename)

    g = ObjModel(model_data)
    g.export_to_obj(output_filename, scale)

    print("Done")



