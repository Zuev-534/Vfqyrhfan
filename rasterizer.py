import pygame
from graph import Vector
from scene import Scene
from vocabulary import GREY1
from order_of_output import *


def cut(scene, order, camera):
    t_o = []
    for item in order:
        x, y, z = item
        x += int(camera.x) - int((16 + 1) / 2)
        y += int(camera.y) - int((16 + 1) / 2)
        z += int(camera.z) - 5
        try:
            if scene.map[x][y][z].vizible:
                t_o.append((x, y, z))
        except:
            pass
    return t_o


class Rasterizer:
    def draw(self, screen: pygame.Surface, scene: Scene, camera: Vector):
        screen.fill(GREY1)
        temp_order = cut(scene, order, camera)
        for item in temp_order:
            x, y, z = item
            scene.map[x][y][z].draw_cube(screen, camera)