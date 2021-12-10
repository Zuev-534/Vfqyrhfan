import pygame
from graph import Vector
from scene import Scene
from vocabulary import GREY1
from graph import Cube


class Rasterizer:
    def draw(self, screen: pygame.Surface, scene: Scene, camera: Vector):
        screen.fill(GREY1)
        for i in range(len(scene.cubes)):
            for j in range(len(scene.cubes[i])):
                for k in range(len(scene.cubes[i][j])):
                    if scene.cubes[i][j][k] == 1:
                        Cube(i, j, k).draw_cube(screen, camera)
