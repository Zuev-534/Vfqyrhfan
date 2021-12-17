import pygame
from graph import Vector
from graph.cube_func import draw_cube_func
from scene import Scene
from vocabulary import GREY1
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
    points = [
        [cam.x + distance * 2, cam.y + distance * 2, 10]
        [cam.x - distance * 2, cam.y + distance * 2, 10]
        [cam.x + distance * 2, cam.y - distance * 2, 10]
        [cam.x - distance * 2, cam.y - distance * 2, 10]
    ]


class Rasterizer:
    def draw(self, screen: pygame.Surface, scene: Scene, camera: Vector, cub_h=1, ):
        screen.fill(GREY1)
        temp_order = cut(scene, order, camera)
        fatline = self.selected_block(camera, scene)
        print(fatline)

        for item in temp_order:
            if fatline == item:
                outline = 3
            else:
                outline = 1
            draw_cube_func(screen, scene.map[item[0]][item[1]][item[2]], *item, camera.x, camera.y, camera.z,
                           camera.an_xz,
                           camera.an_xy, camera.d, camera.dx, camera.dy, camera.dz, cub_h, (camera.an_xy_sin,
                                                                                            camera.an_xz_sin,
                                                                                            camera.an_xy_cos,
                                                                                            camera.an_xz_cos), outline)

    def selected_block(self, cam, scene):
        rx = cam.x
        ry = cam.y
        rz = cam.z
        for i in range(6 * 7):
            rx += cam.dx / 7 / cam.d
            ry += cam.dy / 7 / cam.d
            rz += cam.dz / 7 / cam.d
            print(rx, ry, rz)
            if scene.map[round(rx)][round(ry)][round(rz)]:
                return round(rx), round(ry), round(rz)


if __name__ == "__main__":
    print("This module is not for direct call!")
