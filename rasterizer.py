import pygame
from graph import Vector
from scene import Scene
from vocabulary import GREY1


class Rasterizer:
    def draw(self, screen: pygame.Surface, scene: Scene, camera: Vector):
        screen.fill(GREY1)
        for cube in scene.cubes:
            cube.draw_cube(screen, camera)
