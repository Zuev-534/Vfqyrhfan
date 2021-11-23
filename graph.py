from vocabulary import *


class Vector:
    def __init__(self, x0=0, y0=0, z0=0, d0=0, dx0=0, dy0=0, dz0=0, an_xy0=0, an_xz0=0):
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
        self.dx = vector_nul.x - self.x
        self.dy = vector_nul.y - self.y
        self.dz = vector_nul.z - self.z

    def set_coords_d_from_di(self):
        self.d = sqrt(self.dx ** 2 + self.dy ** 2 + self.dz ** 2)

    def scalar(self, vector_nul):
        return (self.dx * vector_nul.dx + self.dy * vector_nul.dy + self.dy * vector_nul.dy)

    def get_angle_cos(self, vector_nul):
        return self.scalar(vector_nul) / (self.d * vector_nul.d)

    def find_k(self, vector_nul):
        """
        k это отношение длинн между вектором и проекцией другого вектора на него
        v*cos(x)/d
        :return: k
        """
        k = self.d * self.get_angle_cos(vector_nul) / vector_nul.d
        return k

    def get_vector(self, vector_nul):
        """
        получение воктора для вывода на камеру
        :param vector_nul:
        :return:
        """
        k = self.find_k(vector_nul)
        dx = self.dx / k - vector_nul.dx
        dy = self.dy / k - vector_nul.dy
        dz = self.dz / k - vector_nul.dz
        return Vector(dx0=dx, dy0=dy, dz0=dz)

    def rotate_vector(self, fi_xy=0.0, fi_zx=0.0):
        self.dx = self.dx * cos(fi_xy) - self.dy * sin(fi_xy)
        self.dy = self.dx * sin(fi_xy) + self.dy * cos(fi_xy)
        self.dx = self.dx * cos(fi_zx) + self.dz * sin(fi_zx)
        self.dz = - self.dx * sin(fi_zx) + self.dz * cos(fi_zx)

    def coords_to_cam(self):
        self.rotate_vector(-self.an_xy, self.an_xz)
        self.rotate_vector(fi_xy=pi/2)
        return self.dx - WIDTH/2, self.dy - HEIGHT/2


