from math import *
import numpy as np
import pygame
from numpy import sign
from numpy import float32
from pygame.draw import *


WIDTH, HEIGHT = 1200, 720
FPS = 60
k = 0.001  # Чувствительность мыши
leg_force = 0.01
stopper_acceleration = 0.19*leg_force  # На сколько ед\с падают составляющие скорости
mm_o = (WIDTH/2, HEIGHT/2, 0) #Точка центра отрисовки миникарты в окне

znak1 = [ 1, 1, -1, -1]
znak2 = [1, -1, -1, 1]
speed_limit_max = 6*leg_force
speed_limit_min = 0.2*leg_force


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
from decimal import *
getcontext().prec=4
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
    realtime_name_texture = realtime_name_font.render(nm, False, BLACK)
    scrn.blit(realtime_name_texture, (point_x, point_y))

def convert_point(point, O_start):
    """
    Функция, переводящая реальные координаты в пайгеймовские.
    Ест координаты в такой СО, что (0,0,0) это O_start;
    Oz - направлена из экрана на смотрящего;
    Ох - возрастает слева направо;
    Oy - возрастает снизу вверх;
    :param point: кортеж трёх координат в СО, приведенной ниже
    :param O_start: центр координат в окне пайгейма
    :return: только абсцисса и ордината, так преобразованные, чтобы описание функции было верно
    """
    x, y, z= point
    a, b, c = O_start
    x = x + a
    y = -y + b
    return x, y