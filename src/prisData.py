from typing import List
import numpy as np

from filereader3db import get_string, get_as_float_list, get_float


class Part:

    def __init__(self):
        self.parent_name: str = ''
        self.child_name: str = ''
        self.origin_x: float = 0
        self.origin_y: float = 0
        self.origin_z: float = 0
        self.offset_x: float = 0
        self.offset_y: float = 0
        self.offset_z: float = 0
        self.rot_mat_xx: float = 0
        self.rot_mat_xy: float = 0
        self.rot_mat_xz: float = 0
        self.rot_mat_yx: float = 0
        self.rot_mat_yy: float = 0
        self.rot_mat_yz: float = 0
        self.rot_mat_zx: float = 0
        self.rot_mat_zy: float = 0
        self.rot_mat_zz: float = 0
        self.axis_rot_x: float = 0
        self.axis_rot_y: float = 0
        self.axis_rot_z: float = 0
        self.min: float = 0
        self.max: float = 0

    def trans_mat(self):
        rot_matrix = np.zeros((4, 4))

        rot_matrix[0][0] = self.rot_mat_xx
        rot_matrix[0][1] = self.rot_mat_xy
        rot_matrix[0][2] = self.rot_mat_xz

        rot_matrix[1][0] = self.rot_mat_yx
        rot_matrix[1][1] = self.rot_mat_yy
        rot_matrix[1][2] = self.rot_mat_yz

        rot_matrix[2][0] = self.rot_mat_zx
        rot_matrix[2][1] = self.rot_mat_zy
        rot_matrix[2][2] = self.rot_mat_zz

        rot_matrix[0][3] = self.origin_x
        rot_matrix[1][3] = self.origin_y
        rot_matrix[2][3] = self.origin_z

        return rot_matrix


class CmpPartData:

    def __init__(self, inputData: dict):
        self.parts: List[Part] = []
        data: bytearray = inputData['value']
        pos: int = 0
        num_parts = len(data) // 0xD0
        for count in range(num_parts):
            part = Part()
            index = data.find(0, pos, 0x40) - pos
            if index < 0 or index > 0x3f:
                index = 0x3f
            part.parent_name, _ = get_string(data, pos, index)
            pos += 0x40

            index = data.find(0, pos, 0x40) - pos
            if index < 0 or index > 0x3f:
                index = 0x3f
            part.child_name, _ = get_string(data, pos, index)
            pos += 0x40

            part.origin_x, pos = get_float(data, pos)
            part.origin_y, pos = get_float(data, pos)
            part.origin_z, pos = get_float(data, pos)

            part.offset_x, pos = get_float(data, pos)
            part.offset_y, pos = get_float(data, pos)
            part.offset_z, pos = get_float(data, pos)

            part.rot_mat_xx, pos = get_float(data, pos)
            part.rot_mat_xy, pos = get_float(data, pos)
            part.rot_mat_xz, pos = get_float(data, pos)

            part.rot_mat_yx, pos = get_float(data, pos)
            part.rot_mat_yy, pos = get_float(data, pos)
            part.rot_mat_yz, pos = get_float(data, pos)

            part.rot_mat_zx, pos = get_float(data, pos)
            part.rot_mat_zy, pos = get_float(data, pos)
            part.rot_mat_zz, pos = get_float(data, pos)

            part.axis_rot_x, pos = get_float(data, pos)
            part.axis_rot_y, pos = get_float(data, pos)
            part.axis_rot_z, pos = get_float(data, pos)

            part.min, pos = get_float(data, pos)
            part.max, pos = get_float(data, pos)
            self.parts.append(part)

