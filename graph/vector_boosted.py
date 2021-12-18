from numba import njit



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
          vector_nul_d, trigonometry, relative=False):
    if relative:
        self_dx, self_dy, self_dz = self_x, self_y, self_z
    else:
        self_dx, self_dy, self_dz = new_di_in_new_pos_func(self_x, self_y, self_z, vector_nul_x, vector_nul_y,
                                                           vector_nul_z)

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
