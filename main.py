from vocabulary import *
from math import *
import pygame

# from pygame.draw import *


WIDTH, HEIGHT = 1280, 720
FPS = 30
k = 0.01  # Чувствительность мыши

class Camera:
    def __init__(self, x0=0, y0=0, v0, an_xy=0, an_xz=0, h=1.75, pr_pl_rng=0.3):
        self.x = x0
        self.y = y0
        self.vx = v0
        self.vy =v0
        self.an_xy = an_xy
        self.an_xz = an_xz
        self.h = h
        self.focus = pr_pl_rng

    def control(self, order, an_xz = 0, an_xy = 0):
        print(an_xz, an_xy)
        """
        Матрица поворота:
        self.vx = vx * cos(an_xy) - vy * sin(an_xy)
        self.vy = vx * sin(an_xy) + vy * cos(an_xy)
        """
        if order == NOTHING:
            pass
        elif order == ROTATE:
            self.an_xy = (an_xy + self.an_xy) % pi
            self.an_xz = (an_xz + self.an_xz) % pi
        elif order == LEFT:
            self.vx += 5 * sin(self.an_xy)
            self.vy += -5 * cos(self.an_xy)
        elif order == RIGHT:
            self.vx += -5 * sin(self.an_xy)
            self.vy += 5 * cos(self.an_xy)
        elif order == FORWARD:
            self.vx += 5 * cos(self.an_xy)
            self.vy += 5 * sin(self.an_xy)
        elif order == BACKWARD:
            self.vx += -5 * cos(self.an_xy)
            self.vy += -5 * sin(self.an_xy)


def interoperate(input_movement):
    if input_movement.type == pygame.QUIT:
        pygame.quit()
    elif input_movement.type == pygame.KEYDOWN:
        if input_movement.key == pygame.K_ESCAPE:
            pygame.quit()
        elif input_movement.key == pygame.K_a:
            return LEFT, 0, 0
        elif input_movement.key == pygame.K_d:
            return RIGHT, 0, 0
        elif input_movement.key == pygame.K_s:
            return BACKWARD, 0, 0
        elif input_movement.key == pygame.K_w:
            return FORWARD, 0, 0
    elif input_movement.type == pygame.MOUSEMOTION:
        x, y = pygame.mouse.get_pos()
        x, y =  - k * (x - int(WIDTH / 2)), k * (y - int(HEIGHT / 2)) # x = - delta <= ось с пайгейиои не сходится
        pygame.mouse.set_pos([int(WIDTH / 2), int(HEIGHT / 2)])
        return ROTATE, x, y
    else:
        return NOTHING, 0, 0


Victor = Camera()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Test controlling')
# pygame.mouse.set_visible(False)


def coords(cam):
    text_render(screen, "x = " + str(cam.x), 50, 50)
    text_render(screen, "y = " + str(cam.y), 50, 100)
    text_render(screen, "an_xy = " + str(cam.an_xy), 50, 150)
    text_render(screen, "an_xz = " + str(cam.an_xz), 50, 200)

clock = pygame.time.Clock()
while True:
    clock.tick(FPS)
    screen.fill(GREY1)
    for event in pygame.event.get():
        Victor.control(*interoperate(event))
        # print(type(interoperate(event)))
    coords(Victor)
    pygame.display.update()