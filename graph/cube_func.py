from graph import *
from vocabulary import *
from numba import njit


def draw_cube_func(screen, cub_id, x, y, z, cam_x, cam_y, cam_z, cam_an_xz, cam_an_xy,
                   cam_d, cam_dx, cam_dy, cam_dz, cub_h):
    points = set_coords_with_move_func(x, y, z, cub_h)

    if cub_are_vis_or_func(cub_id, x, y, z, cam_x, cam_y, cam_z, cam_dx, cam_dy, cam_dz, cam_d):

        coords_2d = coord2d_func(points, cam_x, cam_y, cam_z, cam_an_xz, cam_an_xy, cam_d)

        if cam_x > x + cub_h / 2:
            draw_square_func(screen, cub_id, coords_2d, i=3)
        elif cam_x < x - cub_h / 2:
            draw_square_func(screen, cub_id, coords_2d, i=2)
        if cam_y > y + cub_h / 2:
            draw_square_func(screen, cub_id, coords_2d, j=3)
        elif cam_y < y - cub_h / 2:
            draw_square_func(screen, cub_id, coords_2d, j=2)
        if cam_z > z + cub_h / 2:
            draw_square_func(screen, cub_id, coords_2d, k=3)
        elif cam_z < z - cub_h / 2:
            draw_square_func(screen, cub_id, coords_2d, k=2)


# проверено(только осмотрел)
def draw_square_func(screen, cub_id, coords_2d, i=0, j=0, k=0):
    pass
    if i == 2 or i == 3:
        polygon(screen, get_color(cub_id),
                [coords_2d[i - 2][0][0],
                 coords_2d[i - 2][0][1],
                 coords_2d[i - 2][1][1],
                 coords_2d[i - 2][1][0]])
        polygon(screen, BLACK,
                [coords_2d[i - 2][0][0],
                 coords_2d[i - 2][0][1],
                 coords_2d[i - 2][1][1],
                 coords_2d[i - 2][1][0]], 1)

    if j == 2 or j == 3:
        polygon(screen, get_color(cub_id),
                [coords_2d[0][j - 2][0],
                 coords_2d[0][j - 2][1],
                 coords_2d[1][j - 2][1],
                 coords_2d[1][j - 2][0]])
        polygon(screen, BLACK,
                [coords_2d[0][j - 2][0],
                 coords_2d[0][j - 2][1],
                 coords_2d[1][j - 2][1],
                 coords_2d[1][j - 2][0]], 1)

    if k == 2 or k == 3:
        polygon(screen, get_color(cub_id),
                [coords_2d[0][0][k - 2],
                 coords_2d[0][1][k - 2],
                 coords_2d[1][1][k - 2],
                 coords_2d[1][0][k - 2]])
        polygon(screen, BLACK,
                [coords_2d[0][0][k - 2],
                 coords_2d[0][1][k - 2],
                 coords_2d[1][1][k - 2],
                 coords_2d[1][0][k - 2]], 1)


# Убрал как непостоянный необязательный фактор пока ошибки не исправлю
def cub_are_vis_or_func(cub_id, x, y, z, cam_x, cam_y, cam_z, cam_dx, cam_dy, cam_dz, cam_d):
    return True
    # if cub_id == 0:
    #     return 0
    # dx, dy, dz = vector.new_di_in_new_pos_func(x, y, z, cam_x, cam_y, cam_z)
    # d = vector.set_coords_d_from_di_func(dx, dy, dz)
    # if vector.get_angle_cos_func(dx, dy, dz, d, cam_dx, cam_dy, cam_dz, cam_d) > 1 / 2:
    #     return True
    # else:
    #     return False


@njit(fastmath=True)
def set_coords_with_move_func(x, y, z, h_cube):
    points = np.zeros((2, 2, 2, 3), dtype=float32)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                points[i][j][k][0] = x + (-1) ** (i + 1) * h_cube / 2
                points[i][j][k][1] = y + (-1) ** (j + 1) * h_cube / 2
                points[i][j][k][2] = z + (-1) ** (k + 1) * h_cube / 2
    return points


if __name__ == "__main__":
    print("This module is not for direct call!")


@njit(fastmath=True)
def coord2d_func(points, cam_x, cam_y, cam_z, cam_an_xz, cam_an_xy, cam_d):
    coords_2d = np.zeros((2, 2, 2, 2), dtype=float32)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                coords_2d[i][j][k] = vector.coords_to_cam_func(
                    *vector.get_vector_func(points[i][j][k][0], points[i][j][k][1],
                                            points[i][j][k][2], cam_x, cam_y, cam_z,
                                            cam_an_xz,
                                            cam_an_xy,
                                            cam_d))
    return coords_2d
