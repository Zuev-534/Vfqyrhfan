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
stopper_acceleration = 0.19 * leg_force  # На сколько ед\с падают составляющие скорости
mm_o = (WIDTH / 2, HEIGHT / 2, 0)  # Точка центра отрисовки миникарты в окне
ground = 9

signature_1 = [1, 1, -1, -1]
signature_2 = [1, -1, -1, 1]
speed_limit_max = 6 * leg_force
speed_limit_min = 0.2 * leg_force

LEFT = "LEFT"
RIGHT = "RIGHT"
BACKWARD = "BACKWARD"
FORWARD = "FORWARD"
ROTATE = "ROTATE"
NOTHING = "NOTHING"

AIR = (50, 150, 50)
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


# можно собрать отдельный файл-библиотеку блоков
def get_color(id):
    """
    return: цвет
    """
    if id == 0:
        return AIR
    if id == 1:
        return WHITE
    if id == 2:
        return BLACK
    if id == 3:
        return RED
    if id == 4:
        return GREEN
    if id == 5:
        return BLUE
    if id == 6:
        return CYAN
    if id == 7:
        return MAGENTA
    if id == 8:
        return YELLOW


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


def convert_point(point, o_start):
    """
    Функция, переводящая реальные координаты в пайгеймовские.
    Ест координаты в такой СО, что (0,0,0) это O_start;
    Oz - направлена из экрана на смотрящего;
    Ох - возрастает слева направо;
    Oy - возрастает снизу вверх;
    :param point: кортеж трёх координат в СО, приведенной ниже
    :param o_start: центр координат в окне пайгейма
    :return: только абсцисса и ордината, так преобразованные, чтобы описание функции было верно
    """
    x, y, z = point
    a, b, c = o_start
    x = x + a
    y = -y + b
    return x, y


def cut(scene, order, camera, d, h):
    t_o = []
    for item in order:
        x, y, z = item
        x += int(camera.x + 0.5) - int(d / 2)
        y += int(camera.y + 0.5) - int(d / 2)
        z += int(camera.z + 0.5) - int(h / 2)
        if scene.map[x][y][z]:
            t_o.append((x, y, z))
    return t_o


if __name__ == "__main__":
    print("This module is not for direct call!")
