#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import struct
from typing import List, Dict


def get_as_int_list(data: bytearray) -> List[int]:
    arr = []
    for i in range(0, len(data), 4):
        arr.append(int.from_bytes(data[i:i+4], sys.byteorder, signed=False))
    return arr


def get_as_float_list(data: bytearray) -> List[float]:
    arr = []
    for i in range(0, len(data), 4):
        arr.append(struct.unpack("f", data[i:i+4])[0])
    return arr


def get_as_string(data: bytearray):
    return data.decode("ASCII")


def get_int(data: bytes, pos: int) -> (int, int):
    return int.from_bytes(data[pos:pos + 4], sys.byteorder, signed=True), pos + 4


def get_string(data:bytes, start_index: int, max_length: int):
    try:
        length = data.index(bytes(0), start_index, start_index+max_length)
    except:
        length = max_length

    start_index += max_length
    t = start_index-max_length
    return data[t:t+length], start_index


class UtfFile:

    def load_utf_file(self, path: str) -> Dict:
        with open(path, mode="br") as file:
            buf = file.read()

        pos = 0
        sig, pos = get_int(buf, pos)
        ver, pos = get_int(buf, pos)

        if sig != 0x20465455 or ver != 0x101:
            raise Exception("Unsupported")

        # get node chink info
        node_block_offset, pos = get_int(buf, pos)
        node_size, pos = get_int(buf, pos)

        unknown1, pos = get_int(buf, pos)
        header_size, pos = get_int(buf, pos)

        # get string chunk info
        string_block_offset, pos = get_int(buf, pos)
        string_block_size, pos = get_int(buf, pos)

        pos += 4

        # get data chunk info

        data_block_offset, pos = get_int(buf, pos)

        base = {}

        # load the nodes recursively
        self.parse_node(buf, node_block_offset, 0, string_block_offset, data_block_offset, base)

        return base

    def parse_node(self, buf: bytes, node_block_start: int, node_start: int, string_block_offset: int, data_block_offset: int,
                   parent: Dict):
        offset: int = node_block_start + node_start
        while True:
            peer_offset, offset = get_int(buf, offset)
            name_offset, offset = get_int(buf, offset)
            flags, offset = get_int(buf, offset)
            zero, offset = get_int(buf, offset)
            child_offset, offset = get_int(buf, offset)
            allocated_size, offset = get_int(buf, offset)
            size, offset = get_int(buf, offset)
            size2, offset = get_int(buf, offset)
            u1, offset = get_int(buf, offset)
            u2, offset = get_int(buf, offset)
            u3, offset = get_int(buf, offset)

            # extract the node name
            length = 0
            for i in range(string_block_offset + name_offset, len(buf)):
                if buf[i] == 0:
                    break
                length += 1

            t = string_block_offset + name_offset
            name = buf[t:t + length].decode("ASCII")

            # extract data if this is a leaf

            data = bytearray(size)
            if (flags & 0xFF) == 0x80:
                if size != size2:
                    print(f"Possible compression being used on {name}")
                t = child_offset + data_block_offset
                data[0:size] = buf[t:t+size]
            else:
                data = bytearray(0)

            node = {'name': name, 'value': data, 'text': name}
            parent[name] = node

            if child_offset > 0 and flags == 0x10:
                self.parse_node(buf, node_block_start, child_offset, string_block_offset, data_block_offset, node)

            if peer_offset == 0:
                break

            offset = node_block_start + peer_offset
