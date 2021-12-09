import pygame
from graph import Vector
from scene import Scene
from vocabulary import GREY1
from order_of_output import *

class Rasterizer:
    def draw(self, screen: pygame.Surface, scene: Scene, camera: Vector):
        screen.fill(GREY1)
        draw_pool = cut(scene.cubes, step, distance)
        for i in range(distance**3 - 1):
