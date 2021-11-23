from math import *
import pygame
from numpy import sign
from pygame.draw import *

WIDTH, HEIGHT = 600, 600
FPS = 30
k = 0.003  # Чувствительность мыши
leg_force = 0.1
stopper_acceleration = 0.3*leg_force  # На сколько ед\с падают составляющие скорости
gravity = 0

znak1 = [ 1, 1, -1, -1]
znak2 = [1, -1, -1, 1]
speed_limit_max = 3*leg_force
speed_limit_min = 0.7*leg_force


LEFT = "LEFT"
RIGHT = "RIGHT"
BACKWARD = "BACKWARD"
FORWARD = "FORWARD"
ROTATE = "ROTATE"
NOTHING = "NOTHING"

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY1 = (180, 180, 180)
# -------------------------------------------------------------------
import pygame
from pygame.draw import *


def text_render(scrn, nm, point_x, point_y):
    """
    Функция, отрисовывающая текст
    :param scrn: поверхность для вывода
    :param nm: текст для вывода
    :param point_x: абсцисса левой верхней точки поверхности
    :param point_y: ордината левой верхней точки поверхности
    :return: ---
    """
    realtime_name_font = pygame.font.SysFont("", 30)
    realtime_name_texture = realtime_name_font.render(nm, False, GREEN)
    scrn.blit(realtime_name_texture, (point_x, point_y))
