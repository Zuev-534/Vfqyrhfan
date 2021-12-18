from vocabulary import *
from numba import njit


def scalar_func(dx, dy, dz, vector_nul_dx, vector_nul_dy, vector_nul_dz):
    return dx * vector_nul_dx + dy * vector_nul_dy + dz * vector_nul_dz


def get_angle_cos_func(dx, dy, dz, d, vector_nul_dx, vector_nul_dy, vector_nul_dz, vector_nul_d):
    return scalar_func(dx, dy, dz, vector_nul_dx, vector_nul_dy, vector_nul_dz) / (d * vector_nul_d)


def set_coords_d_from_di_func(dx, dy, dz):
    return np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)


def new_di_in_new_pos_func(vec_1_x, vec_1_y, vec_1_z, vector_nul_x, vector_nul_y, vector_nul_z):
    dx = -vector_nul_x + vec_1_x
    dy = -vector_nul_y + vec_1_y
    dz = -vector_nul_z + vec_1_z
    return dx, dy, dz


def from_world_to_screen(self_x, self_y, self_z, vector_nul_x, vector_nul_y, vector_nul_z, vector_nul_d, trigonometry):
    self_dx, self_dy, self_dz = new_di_in_new_pos_func(self_x, self_y, self_z, vector_nul_x, vector_nul_y, vector_nul_z)
    return from_relative_to_screen(self_dx, self_dy, self_dz, vector_nul_d, trigonometry)


def from_relative_to_screen(self_dx, self_dy, self_dz, vector_nul_d, trigonometry):
    vector_nul_dx, vector_nul_dy, vector_nul_dz = set_coords_di_from_d(vector_nul_d, trigonometry)
    dx, dy, dz = find_projected_vector(self_dx, self_dy, self_dz, vector_nul_dx, vector_nul_dy, vector_nul_dz,
                                       vector_nul_d)
    dx, dz = transformation_to_screen(dx, dy, dz, trigonometry)
    return WIDTH * (dx / 2 / vector_nul_d + 1 / 2), HEIGHT * (1 - (dz / 2 * np.sqrt(3) / vector_nul_d + 1 / 2))


def gt_vr(self_x, self_y, self_z, vector_nul_x, vector_nul_y, vector_nul_z,
          vector_nul_d, trigonometry):
    self_dx, self_dy, self_dz = new_di_in_new_pos_func(self_x, self_y, self_z, vector_nul_x, vector_nul_y,
                                                       vector_nul_z)

    vector_nul_an_xy_sin, vector_nul_an_xy_cos, vector_nul_an_xz_sin, vector_nul_an_xz_cos = trigonometry

    vector_nul_dx = vector_nul_d * vector_nul_an_xy_cos * vector_nul_an_xz_cos
    vector_nul_dy = vector_nul_d * vector_nul_an_xy_sin * vector_nul_an_xz_cos
    vector_nul_dz = vector_nul_d * vector_nul_an_xz_sin

    l = (self_dx * vector_nul_dx + self_dy * vector_nul_dy + self_dz * vector_nul_dz) \
        / (vector_nul_d * vector_nul_d)

    dx = self_dx / l - vector_nul_dx
    dy = self_dy / l - vector_nul_dy
    dz = self_dz / l - vector_nul_dz
    return dx, dy, dz


def transformation_to_screen(dx, dy, dz, trigonometry):
    dx, dy = dx * trigonometry[1] + dy * trigonometry[0], - dx * trigonometry[0] + dy * trigonometry[1]
    dz = - dx * trigonometry[2] + dz * trigonometry[3]
    return -dy, dz


def set_coords_di_from_d(vector_nul_d, trigonometry):
    return vector_nul_d * trigonometry[1] * trigonometry[3], vector_nul_d * trigonometry[0] * trigonometry[
        3], vector_nul_d * trigonometry[2]


def find_projected_vector(self_dx, self_dy, self_dz, vector_nul_dx, vector_nul_dy, vector_nul_dz, vector_nul_d):
    aspect_ratio = (self_dx * vector_nul_dx + self_dy * vector_nul_dy + self_dz * vector_nul_dz) / (
            vector_nul_d * vector_nul_d)
    dx = self_dx / aspect_ratio - vector_nul_dx
    dy = self_dy / aspect_ratio - vector_nul_dy
    dz = self_dz / aspect_ratio - vector_nul_dz
    return dx, dy, dz


def new_di_in_new_pos_func(self_x, self_y, self_z, vector_nul_x, vector_nul_y, vector_nul_z):
    self_dx = -vector_nul_x + self_x
    self_dy = -vector_nul_y + self_y
    self_dz = -vector_nul_z + self_z
    return self_dx, self_dy, self_dz


def r_v_z(x, y, fi_xy=0.0):
    return x * np.cos(fi_xy) - y * np.sin(fi_xy), x * np.sin(fi_xy) + y * np.cos(fi_xy)


def r_v_y(x, z, fi_zx=0.0):
    return x * np.cos(fi_zx) + z * np.sin(fi_zx), - x * np.sin(fi_zx) + z * np.cos(fi_zx)


def r_v_x(z, y, fi_yz=0.0):
    return y * np.sin(fi_yz) + z * np.cos(fi_yz), y * np.cos(fi_yz) - z * np.sin(fi_yz)
