from __future__ import annotations
from vocabulary import *

from graph import vector_boosted

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
        dx, dy, dz = vector_boosted.gt_vr(self.x, self.y, self.z, vector_nul.x, vector_nul.y, vector_nul.z,
                           vector_nul.an_xz, vector_nul.an_xy, vector_nul.d,
                           (vector_nul.an_xy_sin, vector_nul.an_xz_sin, vector_nul.an_xy_cos, vector_nul.an_xz_cos))
        abc = Vector(dx0=dx, dy0=dy, dz0=dz)
        abc.set_coords_d_from_di()
        return abc

    def rotate_vector_z(self, fi_xy=0.0):
        self.dx, self.dy = vector_boosted.r_v_z(self.dx, self.dy, fi_xy)

    def rotate_vector_y(self, fi_zx=0.0):
        self.dx, self.dz = vector_boosted.r_v_y(self.dx, self.dz, fi_zx)

    def rotate_vector_x(self, fi_yz=0.0):
        self.dz, self.dy =  vector_boosted.r_v_x(self.dz, self.dy, fi_yz)

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

    def min_int_distance(self, scene, cam: Vector, order, ground):
        """
        проверяет нахождение блоков поблизости в кубе 5х5, возвращает 6 чисел в формате,
        какую компоненту скорости нужно убить
        return: [0,0,1,0,0,1]
        """
        ret = [0, 0, 0, 0, 0, 0]
        for item in cut(scene, order, cam, 3, 3):
            dx = item[0] - cam.x
            dy = item[1] - cam.y
            dz = item[2] - cam.z
            if 0 < dx <= 1.45 and abs(dy) <= 0.5 and abs(dz) <= 0.5:
                ret[0] += 1
            elif 0 < dy <= 1.45 and abs(dx) <= 0.5 and abs(dz) <= 0.5:
                ret[1] += 1
            elif 0 < dz <= 1.45 and abs(dx) <= 0.5 and abs(dy) <= 0.5:
                ret[2] += 1
            elif 0 < -dx <= 1.45 and abs(dy) <= 0.5 and abs(dz) <= 0.5:
                ret[3] += 1
            elif 0 < -dy <= 1.45 and abs(dx) <= 0.5 and abs(dz) <= 0.5:
                ret[4] += 1
            elif 0 < -dz <= 1.45 and abs(dx) <= 0.5 and abs(dy) <= 0.5:
                ret[5] += 1
            elif abs(dx) <= 0.5 or abs(dy) <= 0.5 or abs(dz) <= 0.5:
                if sqrt((abs(dx) - 0.5) ** 2 + (abs(dy) - 0.5) ** 2) <= 0.92 and abs(dz) <= 0.5:
                    if dx > 0:
                        ret[0] += 1
                    else:
                        ret[3] += 1
                    if dy > 0:
                        ret[1] += 1
                    else:
                        ret[4] += 1

                if sqrt((abs(dx) - 0.5) ** 2 + (abs(dz) - 0.5) ** 2) <= 0.92 and abs(dy) <= 0.5:
                    if dx > 0:
                        ret[0] += 1
                    else:
                        ret[3] += 1
                    if dz > 0:
                        ret[2] += 1
                    else:
                        ret[5] += 1

                if sqrt((abs(dy) - 0.5) ** 2 + (abs(dz) - 0.5) ** 2) <= 0.92 and abs(dx) <= 0.5:
                    if dy > 0:
                        ret[1] += 1
                    else:
                        ret[4] += 1
                    if dz > 0:
                        ret[2] += 1
                    else:
                        ret[5] += 1
            elif sqrt((abs(dy) - 0.5) ** 2 + (abs(dx) - 0.5) ** 2 + (abs(dz) - 0.5) ** 2) <= 0.89:
                if dx > 0:
                    ret[0] += 1
                else:
                    ret[3] += 1
                if dy > 0:
                    ret[1] += 1
                else:
                    ret[4] += 1
                if dz > 0:
                    ret[2] += 1
                else:
                    ret[5] += 1

        if cam.z <= ground + 1.5:
            ret[5] += 1

        print(ret)
        return ret
