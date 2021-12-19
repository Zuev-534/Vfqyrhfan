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
        """
        Инициализирует игру и всё остальное
        width:ширина экрана
        height: высота экрана
        ground: уровень земли
        """
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
        """
        основной цикл игры, отвечает за порядок вызова всех функций
        return: None
        """
        while self.running:
            self.clock.tick(self.FPS)
            self.player_get_camera = self.player.get_camera()

            for event in pygame.event.get():
                self.update(event)
                self.constr = self.player.update(event, self.scene, self.rasterizer.fat)
            self.player.move(order_of_tuk.order, self.ground, self.scene)

            self.rasterizer.draw(self.screen, self.scene, self.player_get_camera, self.constr)
            self.constr = False
            self.gui(self.player.color)
            pygame.display.update()

        pygame.quit()

    def update(self, event):
        """
        проверяет не нажата ли клавиша выключения программы,
        при необходимости меняет self.running на False
        event: пайгеймовский евент
        return: None
        """
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self.running = False

    def gui(self, color):
        """
        graphic user interface
        отвечает за вывод информации для тестера на экран, за кружочек в центре экрана
        color:цвет в формате от 1 до 8
        return:None
        """
        w, h = self.screen.get_clip().size
        circle(self.screen, get_color(color), (w / 2, h / 2), 6, 2)
        coords(self.screen, self.player, self.clock.get_fps())
