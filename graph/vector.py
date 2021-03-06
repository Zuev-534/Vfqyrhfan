from __future__ import annotations
from vocabulary import *
from graph import vector_boosted


class Vector:
    def __init__(self, x0=0.0, y0=0.0, z0=0.0, d0=0.0, dx0=0.0, dy0=0.0, dz0=0.0, an_xy0=0.0, an_xz0=0.0):
        """
        инициализирует объект класса вектор
        """
        self.d = d0
        self.x = x0
        self.y = y0
        self.z = z0
        self.dx = dx0
        self.dy = dy0
        self.dz = dz0
        self.an_xy = an_xy0
        self.an_xz = an_xz0

        # an_xy_sin, an_xy_cos, an_xz_sin, an_xz_cos
        self.trigonometry_array = np.array([0, 1, 0, 1], dtype='float32')

    @staticmethod
    def from_polar(x, y, z, lng, lat, r):
        """
        задаёт относительные координаты из полярных координат
        return: vector с посчитанными относительными координатами
        """
        vector = Vector(x0=x, y0=y, z0=z, d0=r, an_xy0=lng, an_xz0=lat)
        vector.set_coords_di_from_d()
        return vector

    def set_coords_di_from_d(self):
        """
        задаёт относительные координаты из полярных координат
        return:None
        """
        self.trigonometry_array[0] = np.sin(self.an_xy)
        self.trigonometry_array[1] = np.cos(self.an_xy)
        self.trigonometry_array[2] = np.sin(self.an_xz)
        self.trigonometry_array[3] = np.cos(self.an_xz)
        self.dx, self.dy, self.dz = vector_boosted.set_coords_di_from_d(self.d, self.trigonometry_array)

    def new_di_in_new_pos(self, vector_nul):
        """
        задаёт относительные координаты между двумя точками
        vector_nul: второй вектор
        return: None
        """
        self.dx = -vector_nul.x + self.x
        self.dy = -vector_nul.y + self.y
        self.dz = -vector_nul.z + self.z

    def from_world_to_screen(self, vector_nul):
        """
        выдаёт координаты на экране из абсолютных координат в мире
        vector_nul: точка, которую требуется отрисовать
        return: x, y точки
        """
        self.new_di_in_new_pos(vector_nul)
        dx, dy = vector_boosted.from_relative_to_screen(self.dx, self.dy, self.dz, vector_nul.d,
                                                        vector_nul.trigonometry_array)
        return dx, dy

    def set_coords_d_from_di(self):
        """
        устанавливает d посредством di
        """
        self.d = np.sqrt(self.dx ** 2 + self.dy ** 2 + self.dz ** 2)

    def scalar(self, vector_nul):
        """
        считает скалярное произведение между веторами
        vector_nul:
        return: scalar
        """
        return self.dx * vector_nul.dx + self.dy * vector_nul.dy + self.dz * vector_nul.dz

    def get_angle_cos(self, vector_nul):
        """
        выдаёт косинус между векторами
        vector_nul:второй вектор
        return: cos между векторами
        """
        return self.scalar(vector_nul) / (self.d * vector_nul.d)

    def rotate_vector_z(self, fi_xy=0.0):
        """
        вращает матрицу векторна на угол fi_xy вокруг оси z
        fi_xy: угол поворота
        return: None
        """
        self.dx, self.dy = vector_boosted.r_v_z(self.dx, self.dy, fi_xy)

    def rotate_vector_y(self, fi_zx=0.0):
        """
        вращает матрицу векторна на угол fi_xz вокруг оси y
        fi_zx: угол поворота
        return: None
        """
        self.dx, self.dz = vector_boosted.r_v_y(self.dx, self.dz, fi_zx)

    def rotate_vector_x(self, fi_yz=0.0):
        """
        вращает матрицу вектора на на угол fi_yz вокруг оси x
        fi_yz: угол поворота
        return: None
        """
        self.dz, self.dy = vector_boosted.r_v_x(self.dz, self.dy, fi_yz)

    def print_all(self):
        """
        отладочная функция, выводит все основные данные вектора
        """
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


def check_distance(scene, cam: Vector, order, grnd):
    """
    проверяет нахождение блоков поблизости в кубе 3х3, возвращает 6 чисел в формате,
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
            if np.sqrt((abs(dx) - 0.5) ** 2 + (abs(dy) - 0.5) ** 2) <= 0.92 and abs(dz) <= 0.5:
                if dx > 0:
                    ret[0] += 1
                else:
                    ret[3] += 1
                if dy > 0:
                    ret[1] += 1
                else:
                    ret[4] += 1

            if np.sqrt((abs(dx) - 0.5) ** 2 + (abs(dz) - 0.5) ** 2) <= 0.92 and abs(dy) <= 0.5:
                if dx > 0:
                    ret[0] += 1
                else:
                    ret[3] += 1
                if dz > 0:
                    ret[2] += 1
                else:
                    ret[5] += 1

            if np.sqrt((abs(dy) - 0.5) ** 2 + (abs(dz) - 0.5) ** 2) <= 0.92 and abs(dx) <= 0.5:
                if dy > 0:
                    ret[1] += 1
                else:
                    ret[4] += 1
                if dz > 0:
                    ret[2] += 1
                else:
                    ret[5] += 1
        elif np.sqrt((abs(dy) - 0.5) ** 2 + (abs(dx) - 0.5) ** 2 + (abs(dz) - 0.5) ** 2) <= 0.87:
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

    if cam.z <= grnd + 1.5:
        ret[5] += 1
    if cam.z >= 19:
        ret[2] += 1
    return ret
