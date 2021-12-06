from __future__ import annotations
from vocabulary import *
import pygame


# from numba import njit
#
#
#
# @njit(cache=True, parallel=True, fastmath=True)
# def get_vector(a, d_a, kam, d_kam, an_xy, an_xz, D):
#     d_a = a - kam
#     d_kam[0] = D * np.cos(an_xy) * np.cos(an_xz)
#     d_kam[1] = D * np.sin(an_xy) * np.cos(an_xz)
#     d_kam[2] = D * np.sin(an_xz)
#     l = (np.sum(d_kam * d_a) / np.square(D))
#     d_a = d_a / l - d_kam
#     return (d_a, an_xy, an_xz, D)
#
# # @njit(cache=True, parallel=True, fastmath=True)
# def coords_to_cam(d_a, an_xy, an_zx, D, WIDTH=800, HEIGHT=450):
#     x = d_a[0]
#     y = d_a[1]
#     d_a[0] = x * cos(-an_xy) - y * sin(-an_xy)
#     d_a[1] = x * sin(-an_xy) + y * cos(-an_xy)
#     x = d_a[0]
#     z = d_a[2]
#     d_a[0] = x * cos(an_zx) + z * sin(an_zx)
#     d_a[2] = - x * sin(an_zx) + z * cos(an_zx)
#     x = d_a[0]
#     y = d_a[1]
#     d_a[0] = - y
#     d_a[1] = x
#
#     return ((d_a[0] * WIDTH / 2 / D + WIDTH / 2), (d_a[2] * HEIGHT / 2 * sqrt(3) / D + HEIGHT / 2))
#

# def get_vector(self, self.d, kam, d_kam, an_xy, an_xz):
#     self.dx = -vector_nul.x + self.x
#     self.dy = -vector_nul.y + self.y
#     self.dz = -vector_nul.z + self.z
#     self.d = sqrt(self.dx ** 2 + self.dy ** 2 + self.dz ** 2)
#     vector_nul.dx = vector_nul.d * cos(vector_nul.an_xy) * cos(vector_nul.an_xz)
#     vector_nul.dy = vector_nul.d * sin(vector_nul.an_xy) * cos(vector_nul.an_xz)
#     vector_nul.dz = vector_nul.d * sin(vector_nul.an_xz)
#     self.get_angle_cos(vector_nul)
#     l = (self.dx * vector_nul.dx + self.dy * vector_nul.dy + self.dz * vector_nul.dz) / (vector_nul.d * vector_nul.d)
#     dx = self.dx / l - vector_nul.dx
#     dy = self.dy / l - vector_nul.dy
#     dz = self.dz / l - vector_nul.dz
#     abc = Vector(dx0=dx, dy0=dy, dz0=dz)
#     abc.set_coords_d_from_di()
#     return abc


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

    def set_coords_di_from_d(self):
        self.dx = self.d * cos(self.an_xy) * cos(self.an_xz)
        self.dy = self.d * sin(self.an_xy) * cos(self.an_xz)
        self.dz = self.d * sin(self.an_xz)

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
        self.dx = -vector_nul.x + self.x
        self.dy = -vector_nul.y + self.y
        self.dz = -vector_nul.z + self.z
        self.d = sqrt(self.dx ** 2 + self.dy ** 2 + self.dz ** 2)
        vector_nul.dx = vector_nul.d * cos(vector_nul.an_xy) * cos(vector_nul.an_xz)
        vector_nul.dy = vector_nul.d * sin(vector_nul.an_xy) * cos(vector_nul.an_xz)
        vector_nul.dz = vector_nul.d * sin(vector_nul.an_xz)
        l = (self.dx * vector_nul.dx + self.dy * vector_nul.dy + self.dz * vector_nul.dz) \
            / (vector_nul.d * vector_nul.d)
        dx = self.dx / l - vector_nul.dx
        dy = self.dy / l - vector_nul.dy
        dz = self.dz / l - vector_nul.dz
        abc = Vector(dx0=dx, dy0=dy, dz0=dz)
        abc.set_coords_d_from_di()
        return abc

    def rotate_vector_z(self, fi_xy=0.0):
        x = self.dx
        y = self.dy
        self.dx = x * cos(fi_xy) - y * sin(fi_xy)
        self.dy = x * sin(fi_xy) + y * cos(fi_xy)

    def rotate_vector_y(self, fi_zx=0.0):
        x = self.dx
        z = self.dz
        self.dx = x * cos(fi_zx) + z * sin(fi_zx)
        self.dz = - x * sin(fi_zx) + z * cos(fi_zx)

    def rotate_vector_x(self, fi_yz=0.0):
        z = self.dz
        y = self.dy
        self.dz = y * sin(fi_yz) + z * cos(fi_yz)
        self.dy = y * cos(fi_yz) - z * sin(fi_yz)

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

        return ((self.dx * WIDTH / 2 / cam.d + WIDTH / 2), (self.dz * HEIGHT / 2 * sqrt(3) / cam.d + HEIGHT / 2))
