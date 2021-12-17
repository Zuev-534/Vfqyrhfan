import pygame
from graph import Vector
from graph import vector
from graph.cube_func import draw_cube_func
from scene import Scene
from vocabulary import GREY1, WIDTH, HEIGHT
from order_of_output import *


def cut(scene, order, camera):
    t_o = []
    for item in order:
        x, y, z = item
        x += int(camera.x + 0.5) - int(distance / 2)
        y += int(camera.y + 0.5) - int(distance / 2)
        z += int(camera.z + 0.5) - int(h_dis / 2)
        try:
            if scene.map[x][y][z]:
                t_o.append((x, y, z))
        except:
            pass
    return t_o


def draw_bottom(screen, cam):
    x_ground, y_ground = vector.coords_to_cam_func(
        *vector.get_vector_func(100000, 100000, 9, cam.x, cam.y, cam.z, cam.an_xz, cam.an_xy, cam.d, (cam.an_xy_sin,
                                                                                                      cam.an_xz_sin,
                                                                                                      cam.an_xy_cos,
                                                                                                      cam.an_xz_cos)))
    pygame.draw.polygon(screen, (50, 150, 50), [[0, y_ground], [WIDTH, y_ground], [WIDTH, HEIGHT], [0, HEIGHT]])


class Rasterizer:
    def draw(self, screen: pygame.Surface, scene: Scene, camera: Vector, cub_h=1, ):
        screen.fill(GREY1)
        temp_order = cut(scene, order, camera)
        fatline = self.selected_block(camera, scene)
        draw_bottom(screen, camera)
        outline = 1
        if type(fatline) == type((1, 2, 3)):
            if fatline[3]:
                outline = 3
                draw_cube_func(screen, scene.map[fatline[0]][fatline[1]][fatline[2]], fatline[0], fatline[1], fatline[2],
                               camera.x, camera.y,
                               camera.z,
                               camera.an_xz,
                               camera.an_xy, camera.d, camera.dx, camera.dy, camera.dz, cub_h, (camera.an_xy_sin,
                                                                                                camera.an_xz_sin,
                                                                                                camera.an_xy_cos,
                                                                                                camera.an_xz_cos), outline,
                               grnd=fatline[3])
                outline = 1
        for item in temp_order:
            if type(fatline) == type((1, 2, 3)):
                if fatline[:-1] == item:
                    outline = 3
            draw_cube_func(screen, scene.map[item[0]][item[1]][item[2]], *item, camera.x, camera.y, camera.z,
                           camera.an_xz,
                           camera.an_xy, camera.d, camera.dx, camera.dy, camera.dz, cub_h, (camera.an_xy_sin,
                                                                                            camera.an_xz_sin,
                                                                                            camera.an_xy_cos,
                                                                                            camera.an_xz_cos), outline)
            outline = 1


    def selected_block(self, cam, scene):
        rx = cam.x
        ry = cam.y
        rz = cam.z
        for i in range(6 * 7):
            rx += cam.dx / 7 / cam.d
            ry += cam.dy / 7 / cam.d
            rz += cam.dz / 7 / cam.d
            if scene.map[round(rx)][round(ry)][round(rz)]:
                return round(rx), round(ry), round(rz), False
            if round(rz) == 9:
                return round(rx), round(ry), round(rz), True


if __name__ == "__main__":
    print("This module is not for direct call!")
