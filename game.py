import pygame
from time import time
from player import coords, Player
from pygame.draw import circle
from vocabulary import *
from scene import Scene
from itertools import chain
from graph import Vector, vector_boosted
from math import sin, cos
from rasterizer import Rasterizer
import order_of_tuk



class Game:
    def __init__(self, width, height, ground):
        import order_of_output
        self.FPS = 60
        self.gravity = -0.003
        self.ground = ground
        pygame.init()
        pygame.display.set_caption('Test controlling')
        pygame.mouse.set_visible(False)

        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.scene = Scene()
        self.scene.test()

        self.player = Player((50, 50, 12), self.gravity, (width, height))
        self.rasterizer = Rasterizer()
        self.player_get_camera = None
        self.constr = False

    def loop(self):
        while self.running:
            self.clock.tick(self.FPS)
            self.player_get_camera = self.player.get_camera()

            for event in pygame.event.get():
                self.update(event)
                self.constr = self.player.update(event, self.scene, self.rasterizer.fat)
            self.player.move(order_of_tuk.order, self.ground, self.scene)

            self.rasterizer.draw(self.screen, self.scene, self.player_get_camera, self.constr)
            self.constr = False

            self.log()
            self.gui()
            pygame.display.update()

        pygame.quit()

    def update(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self.running = False

    def gui(self):
        w, h = self.screen.get_clip().size
        circle(self.screen, BLACK, (w / 2, h / 2), 4, 1)

    def log(self):

        clip = self.screen.get_clip()
        center = (clip.w / 2, clip.h / 2, 0)

        camera = self.player.get_camera()

        u = 15
        pygame.draw.lines(self.screen, WHITE, True, [
            convert_point((camera.x, camera.y, 0), center),
            convert_point((
                camera.x + u * cos(camera.an_xy),
                camera.y + u * sin(camera.an_xy),
                0,
            ), center),
        ], 2)

        coords(self.screen, self.player, self.clock.get_fps())
