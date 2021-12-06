from vocabulary import *
from graph import Vector
import pygame


class Player:
    def __init__(self, r: pygame.Vector3, g: float):
        self.vector = Vector(x0=r.x, y0=r.y, z0=r.z)
        self.v = pygame.Vector3()
        self.a = pygame.Vector3(0, 0, g)
        self.h = 1.75
        self.vector.d = 10
        self.controlling = [0, 0, 0, 0, 0, 0, 0]
        # LEFT, RIGHT, BACKWARD, FORWARD, ROTATE, an_xy, an_zx

    def get_camera(self) -> Vector:
        return self.vector

    def control(self, an_xz=0, an_xy=0):
        """
        Механика движения камеры.
        :param an_xz: угол в вертикальной плоскости (нужно уточнить направление)
        :param an_xy: угол в горизонтальной плоскости
        :return: ---
        """
        # Матрица повороооота:
        # self.vx = vx * cos(an_xy) - vy * sin(an_xy)
        # self.vy = vx * sin(an_xy) + vy * cos(an_xy)

        # for i in range(3):
        #     if self.controlling[i]:
        #         self.ax += znak1[i] * 0.5 * cos(self.an_xy)
        #         self.ay += znak2[i] * 0.5 * sin(self.an_xy)
        self.a = pygame.Vector3()
        v_horizontal = self.v.xy.length()
        if v_horizontal > speed_limit_min:
            # self.ay = - self.vy/sqrt(self.vx ** 2 + self.vy ** 2) * stopper_acceleration * 10 ** (
            #             sqrt(self.vx ** 2 + self.vy ** 2) / speed_limit_max / 100 + 0.05)
            # self.ax = - self.vx/sqrt(self.vx ** 2 + self.vy ** 2) * stopper_acceleration * 10 ** (
            #             sqrt(self.vx ** 2 + self.vy ** 2) / speed_limit_max / 100 + 0.05)
            self.a.y = -self.v.y / v_horizontal * stopper_acceleration
            self.a.x = -self.v.x / v_horizontal * stopper_acceleration
        else:
            self.a.x = 0
            self.a.y = 0
        if self.controlling[0]:
            self.a.x += leg_force * sin(self.vector.an_xy)
            self.a.y += -leg_force * cos(self.vector.an_xy)
        if self.controlling[1]:
            self.a.x += -leg_force * sin(self.vector.an_xy)
            self.a.y += leg_force * cos(self.vector.an_xy)
        if self.controlling[3]:
            self.a.x += leg_force * cos(self.vector.an_xy)
            self.a.y += leg_force * sin(self.vector.an_xy)
        if self.controlling[2]:
            self.a.x += -leg_force * cos(self.vector.an_xy)
            self.a.y += -leg_force * sin(self.vector.an_xy)
        if self.controlling[4]:
            self.vector.an_xy = (self.controlling[5] + self.vector.an_xy + pi) % (pi * 2) - pi
            self.vector.an_xz = (self.controlling[6] + self.vector.an_xz)
            if self.vector.an_xz > pi / 2:
                self.vector.an_xz = pi / 2
            if self.vector.an_xz < -pi / 2:
                self.vector.an_xz = -pi / 2
            self.controlling[4], self.controlling[5], self.controlling[6] = 1, 0, 0

    def move(self):
        self.vector.x += self.v.x
        self.vector.y += self.v.y
        self.vector.z += self.v.z
        self.v += self.a
        v_horizontal = self.v.xy.length()
        if v_horizontal > speed_limit_max:
            self.v.x *= speed_limit_max / v_horizontal
            self.v.y *= speed_limit_max / v_horizontal
        if abs(self.v.x) <= speed_limit_min:
            self.v.x = 0
        if abs(self.v.y) <= speed_limit_min:
            self.v.y = 0

    def interoperate(self, input_movement):
        # LEFT, RIGHT, BACKWARD, FORWARD, ROTATE, an_xy, an_xz - controlling
        if input_movement.type == pygame.QUIT:
            pygame.quit()
        elif input_movement.type == pygame.KEYDOWN:
            if input_movement.key == pygame.K_ESCAPE:
                pygame.quit()
            if input_movement.key == pygame.K_d:
                self.controlling[0] = 1
            if input_movement.key == pygame.K_a:
                self.controlling[1] = 1
            if input_movement.key == pygame.K_s:
                self.controlling[2] = 1
            if input_movement.key == pygame.K_w:
                self.controlling[3] = 1
            if input_movement.key == pygame.K_SPACE:
                self.vector.z -= 1
            if input_movement.key == pygame.K_z:
                self.vector.z += 1

        elif input_movement.type == pygame.KEYUP:
            if input_movement.key == pygame.K_d:
                self.controlling[0] = 0
            if input_movement.key == pygame.K_a:
                self.controlling[1] = 0
            if input_movement.key == pygame.K_s:
                self.controlling[2] = 0
            if input_movement.key == pygame.K_w:
                self.controlling[3] = 0
        elif input_movement.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            x, y = - k * (x - int(WIDTH / 2)), k * (y - int(HEIGHT / 2))  # x = - delta <= ось с пайгейиои не сходится
            pygame.mouse.set_pos([int(WIDTH / 2), int(HEIGHT / 2)])
            self.controlling[4], self.controlling[5], self.controlling[6] = 1, x, y


def coords(screen, player: Player, fps):
    text_render(screen, "FPS = " + str(fps)[:4], 50, 10)
    text_render(screen, "x = " + str(player.vector.x)[:4], 50, 30)
    text_render(screen, "y = " + str(player.vector.y)[:4], 50, 60)
    text_render(screen, "z = " + str(player.vector.z)[:4], 50, 90)
    text_render(screen, "vx = " + str(player.v.x * 10)[:4], 50, 120)
    text_render(screen, "vy = " + str(player.v.y * 10)[:4], 50, 150)
    text_render(screen, "vz = " + str(player.v.z * 10)[:4], 50, 180)
    text_render(screen, "ax = " + str(player.a.x * 100)[:4], 50, 210)
    text_render(screen, "ay = " + str(player.a.y * 100)[:4], 50, 240)
    text_render(screen, "az = " + str(player.a.z * 100)[:4], 50, 270)
    text_render(screen, "an_xy = " + str(player.vector.an_xy)[:4], 50, 300)
    text_render(screen, "an_xz = " + str(player.vector.an_xz)[:4], 50, 330)
    text_render(screen, str(player.controlling), 50, 360)
