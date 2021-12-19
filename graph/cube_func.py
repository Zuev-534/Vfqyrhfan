from vocabulary import *
from numba import njit
from graph import vector_boosted


def draw_cube_func(screen, cub_id, x, y, z, cam_x, cam_y, cam_z,
                   cam_d, cub_h, trigonometry, outline, grnd=False):
    points = set_coords_with_move_func(x, y, z, cub_h)

    coords_2d, condition = coord2d_func(points, cam_x, cam_y, cam_z, cam_d, trigonometry)
    if condition:
        if grnd:
            draw_square_func(screen, 0, coords_2d, k=3, out_line=outline)
        else:
            if cam_x > x + cub_h / 2:
                draw_square_func(screen, cub_id, coords_2d, i=3, out_line=outline)
            elif cam_x < x - cub_h / 2:
                draw_square_func(screen, cub_id, coords_2d, i=2, out_line=outline)
            if cam_y > y + cub_h / 2:
                draw_square_func(screen, cub_id, coords_2d, j=3, out_line=outline)
            elif cam_y < y - cub_h / 2:
                draw_square_func(screen, cub_id, coords_2d, j=2, out_line=outline)
            if cam_z > z + cub_h / 2:
                draw_square_func(screen, cub_id, coords_2d, k=3, out_line=outline)
            elif cam_z < z - cub_h / 2:
                draw_square_func(screen, cub_id, coords_2d, k=2, out_line=outline)


# проверено(только осмотрел)
def draw_square_func(screen, cub_id, coords_2d, i=0, j=0, k=0, out_line=1):
    if i == 2 or i == 3:
        lightness = 0.8
        polygon(screen, mult(get_color(cub_id), lightness),
                [coords_2d[i - 2][0][0],
                 coords_2d[i - 2][0][1],
                 coords_2d[i - 2][1][1],
                 coords_2d[i - 2][1][0]])
        polygon(screen, BLACK,
                [coords_2d[i - 2][0][0],
                 coords_2d[i - 2][0][1],
                 coords_2d[i - 2][1][1],
                 coords_2d[i - 2][1][0]], out_line)

    if j == 2 or j == 3:
        lightness = 0.8
        polygon(screen, mult(get_color(cub_id), lightness),
                [coords_2d[0][j - 2][0],
                 coords_2d[0][j - 2][1],
                 coords_2d[1][j - 2][1],
                 coords_2d[1][j - 2][0]])
        polygon(screen, BLACK,
                [coords_2d[0][j - 2][0],
                 coords_2d[0][j - 2][1],
                 coords_2d[1][j - 2][1],
                 coords_2d[1][j - 2][0]], out_line)

    if k == 2 or k == 3:
        if k == 2:
            lightness = 0.7
        else:
            lightness = 0.9
        polygon(screen, mult(get_color(cub_id), lightness),
                [coords_2d[0][0][k - 2],
                 coords_2d[0][1][k - 2],
                 coords_2d[1][1][k - 2],
                 coords_2d[1][0][k - 2]])
        polygon(screen, BLACK,
                [coords_2d[0][0][k - 2],
                 coords_2d[0][1][k - 2],
                 coords_2d[1][1][k - 2],
                 coords_2d[1][0][k - 2]], out_line)

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
def coord2d_func(points, cam_x, cam_y, cam_z, cam_d, trigonometry):
    coords_2d = np.zeros((2, 2, 2, 2), dtype=float32)
    condition = True
    for i in range(2):
        for j in range(2):
            for k in range(2):
                temp = True
                if condition:
                    coords_2d[i][j][k][0], coords_2d[i][j][k][1], temp = vector_boosted.from_world_to_screen(
                        points[i][j][k][0], points[i][j][k][1],
                        points[i][j][k][2], cam_x, cam_y, cam_z, cam_d,
                        trigonometry)
                condition = temp and condition
    return coords_2d, condition
