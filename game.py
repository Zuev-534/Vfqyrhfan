import pygame
from time import time
from player import coords, Player
from pygame.draw import circle
from vocabulary import BLACK, WHITE, GREY1, convert_point
from scene import Scene
from itertools import chain
from graph import Cube, Vector
from math import sin, cos
from rasterizer import Rasterizer


class Game:
    def __init__(self, width, height):
        self.FPS = 60
        self.gravity = 0

        pygame.init()
        pygame.display.set_caption('Test controlling')
        pygame.mouse.set_visible(False)

        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.scene = Scene(
            list(chain.from_iterable([[Cube(15 + 4 * i, 3 + 5 * j, 3) for i in range(20)] for j in range(30)] +
                                     [[Cube(15 + 4 * i, 3 + 5 * j, 8) for i in range(20)] for j in range(30)])),
        )
        self.player = Player(pygame.Vector3(50, 50, 10), self.gravity)
        self.rasterizer = Rasterizer()

    def loop(self):
        while self.running:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                self.update(event)
                self.player.update(event)
            self.player.move()

            self.rasterizer.draw(self.screen, self.scene, self.player.get_camera())

            self.log()

            pygame.display.update()

        pygame.quit()

    def update(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self.running = False

    def log(self):

        circle(self.screen, BLACK,
               Vector(10, 100, 0).get_vector(self.player.get_camera()).coords_to_cam(self.player.get_camera()), 10)
        circle(self.screen, BLACK, Vector(100, 111, 2000000).get_vector(self.player.get_camera()).coords_to_cam(
            self.player.get_camera()), 10)

        clip = self.screen.get_clip()
        center = (clip.w / 2, clip.h / 2, 0)

        camera = self.player.get_camera()
        circle(self.screen, BLACK, convert_point((camera.x, camera.y, 0), center), 5)
        circle(self.screen, BLACK, convert_point((10, 100, 0), center), 5)
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
