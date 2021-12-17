from __future__ import annotations
from vocabulary import *
from numba import njit
import numpy as np
import math


@njit(fastmath=True)
def scalar_func(dx, dy, dz, vector_nul_dx, vector_nul_dy, vector_nul_dz):
    return dx * vector_nul_dx + dy * vector_nul_dy + dz * vector_nul_dz


@njit(fastmath=True)
def get_angle_cos_func(dx, dy, dz, d, vector_nul_dx, vector_nul_dy, vector_nul_dz, vector_nul_d):
    return scalar_func(dx, dy, dz, vector_nul_dx, vector_nul_dy, vector_nul_dz) / (d * vector_nul_d)


@njit(fastmath=True)
def set_coords_d_from_di_func(dx, dy, dz):
    return sqrt(dx ** 2 + dy ** 2 + dz ** 2)


@njit(fastmath=True)
def new_di_in_new_pos_func(vec_1_x, vec_1_y, vec_1_z, vector_nul_x, vector_nul_y, vector_nul_z):
    dx = -vector_nul_x + vec_1_x
    dy = -vector_nul_y + vec_1_y
    dz = -vector_nul_z + vec_1_z
    return dx, dy, dz


@njit(fastmath=True)
def get_vector_func(x, y, z, c_x, c_y, c_z, c_an_xz, c_an_xy, c_d, trigonometry):
    dx, dy, dz = gt_vr(x, y, z, c_x, c_y, c_z, c_an_xz, c_an_xy, c_d, trigonometry)
    return dx, dy, dz, c_an_xy, c_an_xz, c_d, trigonometry


@njit(fastmath=True)
def coords_to_cam_func(abc_dx, abc_dy, abc_dz, cam_an_xy, cam_an_xz, cam_d, trigonometry):
    cam_an_xy_sin, cam_an_xz_sin, cam_an_xy_cos, cam_an_xz_cos = trigonometry
    abc_dx, abc_dy = abc_dx * cam_an_xy_cos + abc_dy * cam_an_xy_sin, (
        -1) * abc_dx * cam_an_xy_sin + abc_dy * cam_an_xy_cos
    abc_dx, abc_dz = abc_dx * cam_an_xz_cos + abc_dz * cam_an_xz_sin, - abc_dx * cam_an_xz_sin + abc_dz * cam_an_xz_cos
    abc_dx, abc_dy = - abc_dy, abc_dx

    return WIDTH * (abc_dx / 2 / cam_d + 1 / 2), HEIGHT * (1 - (abc_dz / 2 * sqrt(3) / cam_d + 1 / 2))


@njit(fastmath=True)
def gt_vr(self_x, self_y, self_z, vector_nul_x, vector_nul_y, vector_nul_z, vector_nul_an_xz, vector_nul_an_xy,
          vector_nul_d, trigonometry, relative = False):
    if relative:
        self_dx, self_dy, self_dz = self_x, self_y, self_z
    else:
        self_dx, self_dy, self_dz = new_di_in_new_pos_func(self_x, self_y, self_z, vector_nul_x, vector_nul_y, vector_nul_z)

    vector_nul_an_xy_sin, vector_nul_an_xz_sin, vector_nul_an_xy_cos, vector_nul_an_xz_cos = trigonometry

    vector_nul_dx = vector_nul_d * vector_nul_an_xy_cos * vector_nul_an_xz_cos
    vector_nul_dy = vector_nul_d * vector_nul_an_xy_sin * vector_nul_an_xz_cos
    vector_nul_dz = vector_nul_d * vector_nul_an_xz_sin

    l = (self_dx * vector_nul_dx + self_dy * vector_nul_dy + self_dz * vector_nul_dz) \
        / (vector_nul_d * vector_nul_d)

    dx = self_dx / l - vector_nul_dx
    dy = self_dy / l - vector_nul_dy
    dz = self_dz / l - vector_nul_dz
    return dx, dy, dz

@njit(fastmath=True)
def new_di_in_new_pos_func(self_x, self_y, self_z, vector_nul_x, vector_nul_y, vector_nul_z):
    self_dx = -vector_nul_x + self_x
    self_dy = -vector_nul_y + self_y
    self_dz = -vector_nul_z + self_z
    return self_dx, self_dy, self_dz

@njit(fastmath=True)
def r_v_z(x, y, fi_xy=0.0):
    return x * cos(fi_xy) - y * sin(fi_xy), x * sin(fi_xy) + y * cos(fi_xy)


@njit(fastmath=True)
def r_v_y(x, z, fi_zx=0.0):
    return x * cos(fi_zx) + z * sin(fi_zx), - x * sin(fi_zx) + z * cos(fi_zx)


@njit(fastmath=True)
def r_v_x(z, y, fi_yz=0.0):
    return y * sin(fi_yz) + z * cos(fi_yz), y * cos(fi_yz) - z * sin(fi_yz)


class Vector:
    def __init__(self, x0=0.0, y0=0.0, z0=0.0, d0=0.0, dx0=0.0, dy0=0.0, dz0=0.0, an_xy0=0.0, an_xz0=0.0):
        self.d = d0
        self.x = x0
        self.y = y0
        self.z = z0
        self.dx = dx0
        self.dy = dy0
        self.dz = dz0
        self.an_xy = an_xy0
        self.an_xz = an_xz0
        self.an_xz_cos = 0
        self.an_xy_cos = 0
        self.an_xz_sin = 0
        self.an_xy_sin = 0

    @staticmethod
    def from_polar(x, y, z, lng, lat, r):
        vector = Vector(x0=x, y0=y, z0=z, d0=r, an_xy0=lng, an_xz0=lat)
        vector.set_coords_di_from_d()
        return vector

    # @staticmethod
    # def from_decart

    def set_coords_di_from_d(self):
        self.an_xz_cos = cos(self.an_xz)
        self.an_xy_cos = cos(self.an_xy)
        self.an_xz_sin = sin(self.an_xz)
        self.an_xy_sin = sin(self.an_xy)
        self.dx = self.d * self.an_xy_cos * self.an_xz_cos
        self.dy = self.d * self.an_xy_sin * self.an_xz_cos
        self.dz = self.d * self.an_xz_sin

    def new_di_in_new_pos(self, vector_nul):
        self.dx = -vector_nul.x + self.x
        self.dy = -vector_nul.y + self.y
        self.dz = -vector_nul.z + self.z

    # def SPEEEED(self, vector_nul):
    #     obj = np.array([self.x, self.y, self.z], dtype=float32)
    #     kam = np.array([vector_nul.x, vector_nul.y, vector_nul.z], dtype=float32)
    #     d_obj = np.zeros(3, dtype=float32)
    #     d_kam = np.zeros(3, dtype=float32)
    #     return (obj, d_obj, kam, d_kam, vector_nul.an_xy, vector_nul.an_xz, vector_nul.d)

    def set_coords_d_from_di(self):
        self.d = sqrt(self.dx ** 2 + self.dy ** 2 + self.dz ** 2)

    def scalar(self, vector_nul):
        return self.dx * vector_nul.dx + self.dy * vector_nul.dy + self.dz * vector_nul.dz

    def get_angle_cos(self, vector_nul):
        return self.scalar(vector_nul) / (self.d * vector_nul.d)

    def find_l(self, vector_nul: Vector):
        """
        l это отношение длинн между вектором и проекцией другого вектора на него
        v*cos(x)/d
        :return: l
        """
        self.new_di_in_new_pos(vector_nul)
        self.set_coords_d_from_di()
        vector_nul.set_coords_di_from_d()
        l = self.d * self.get_angle_cos(vector_nul) / vector_nul.d
        return l

    def get_vector(self, vector_nul: Vector) -> Vector:
        dx, dy, dz = gt_vr(self.x, self.y, self.z, vector_nul.x, vector_nul.y, vector_nul.z,
                           vector_nul.an_xz, vector_nul.an_xy, vector_nul.d,
                           (vector_nul.an_xy_sin, vector_nul.an_xz_sin, vector_nul.an_xy_cos, vector_nul.an_xz_cos))
        abc = Vector(dx0=dx, dy0=dy, dz0=dz)
        abc.set_coords_d_from_di()
        return abc

    def rotate_vector_z(self, fi_xy=0.0):
        self.dx, self.dy = r_v_z(self.dx, self.dy, fi_xy)

    def rotate_vector_y(self, fi_zx=0.0):
        self.dx, self.dz = r_v_y(self.dx, self.dz, fi_zx)

    def rotate_vector_x(self, fi_yz=0.0):
        self.dz, self.dy = r_v_x(self.dz, self.dy, fi_yz)

    def print_all(self):
        print("self = ", self)
        print("d = ", self.d)
        print("x = ", self.x)
        print("y = ", self.y)
        print("z = ", self.z)
        print("dx = ", self.dx)
        print("dy = ", self.dy)
        print("dz = ", self.dz)
        print("an_xy = ", self.an_xy)
        print("an_xy = ", self.an_xz)

    def coords_to_cam(self, cam: Vector):
        self.rotate_vector_z(-cam.an_xy)
        self.rotate_vector_y(cam.an_xz)
        self.rotate_vector_z(fi_xy=pi / 2)

        return WIDTH * (self.dx / 2 / cam.d + 1 / 2), HEIGHT * (1 - (self.dz / 2 * sqrt(3) / cam.d + 1 / 2))
