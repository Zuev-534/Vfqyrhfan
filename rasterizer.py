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
        x += int(camera.x + 0.5) - int((distance) / 2)
        y += int(camera.y + 0.5) - int((distance) / 2)
        z += int(camera.z + 0.5) - int(h_dis / 2)
        try:
            if scene.map[x][y][z]:
                t_o.append((x, y, z))
        except:
            pass
    return t_o


class Rasterizer:
    def draw(self, screen: pygame.Surface, scene: Scene, camera: Vector, cub_h=1):
        screen.fill(GREY1)
        temp_order = cut(scene, order, camera)
        for item in temp_order:
            x, y, z = item
            draw_cube_func(screen, scene.map[x][y][z], x, y, z, camera.x, camera.y, camera.z, camera.an_xz,
                           camera.an_xy, camera.d, camera.dx, camera.dy, camera.dz, cub_h)