import pygame
from time import time
from player import coords, Player
from pygame.draw import circle
from vocabulary import *
from scene import Scene
from itertools import chain
from graph import Cube, Vector
from math import sin, cos
from rasterizer import Rasterizer
import order_of_tuk



class Game:
    def __init__(self, width, height, ground):
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

        self.player = Player(Vector(500, 500, 12), self.gravity)
        self.rasterizer = Rasterizer()
        self.player_get_camera = None

    def loop(self):
        while self.running:
            self.clock.tick(self.FPS)
            self.player_get_camera = self.player.get_camera()

            for event in pygame.event.get():
                self.update(event)
                self.player.update(event)
            self.player.move(self.player_get_camera, order_of_tuk.order, self.ground, self.scene)

            self.rasterizer.draw(self.screen, self.scene, self.player_get_camera)

            self.log()
            self.GUI()
            pygame.display.update()

        pygame.quit()

    def update(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self.running = False

    def GUI(self):
        circle(self.screen, BLACK, (WIDTH / 2, HEIGHT / 2), 4, 1)

    def log(self):

        circle(self.screen, BLACK,
               Vector(510, 521, 10).get_vector(self.player.get_camera()).coords_to_cam(self.player.get_camera()), 10)
        circle(self.screen, BLACK, Vector(500, 500, 200000).get_vector(self.player.get_camera()).coords_to_cam(
            self.player.get_camera()), 10)

        clip = self.screen.get_clip()
        center = (clip.w / 2, clip.h / 2, 0)

        camera = self.player.get_camera()
        circle(self.screen, BLACK, convert_point((camera.x, camera.y, 0), center), 5)
        circle(self.screen, BLACK, convert_point((10, 21, 10), center), 5)
        circle(self.screen, BLACK, convert_point((100, 111, 0), center), 5)

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
