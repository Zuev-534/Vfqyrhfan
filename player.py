from vocabulary import *
from graph import Vector
import pygame


class Player:
    def __init__(self, r: pygame.Vector3, g: float):
        self.vector = Vector(x0=r.x, y0=r.y, z0=r.z)
        self.r = r
        self.v = pygame.Vector3()
        self.a = pygame.Vector3(0, 0, g)
        self.h = 1.75

        self.control_keys = [pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d]
        self.pressed_keys = []

    def get_camera(self) -> Vector:
        self.vector.x = self.r.x
        self.vector.y = self.r.y
        self.vector.z = self.r.z
        self.vector.d = 10
        self.vector.set_coords_di_from_d()
        return self.vector

    def control(self):
        """
        Механика движения камеры.
        :param an_xz: угол в вертикальной плоскости (нужно уточнить направление)
        :param an_xy: угол в горизонтальной плоскости
        :return: ---
        """
        # Матрица повороооота:
        # self.vx = vx * cos(an_xy) - vy * sin(an_xy)
        # self.vy = vx * sin(an_xy) + vy * cos(an_xy)

    def move(self):
        self.a = pygame.Vector3()
        v_horizontal = self.v.xy.length()
        if v_horizontal > speed_limit_min:
            self.a.y = -self.v.y / v_horizontal * stopper_acceleration
            self.a.x = -self.v.x / v_horizontal * stopper_acceleration
        else:
            self.a.x = 0
            self.a.y = 0

        for key in self.pressed_keys:
            if key == pygame.K_d:
                self.a.x += +leg_force * sin(self.vector.an_xy)
                self.a.y += -leg_force * cos(self.vector.an_xy)
            elif key == pygame.K_a:
                self.a.x += -leg_force * sin(self.vector.an_xy)
                self.a.y += +leg_force * cos(self.vector.an_xy)
            elif key == pygame.K_s:
                self.a.x += -leg_force * cos(self.vector.an_xy)
                self.a.y += -leg_force * sin(self.vector.an_xy)
            elif key == pygame.K_w:
                self.a.x += +leg_force * cos(self.vector.an_xy)
                self.a.y += +leg_force * sin(self.vector.an_xy)

        self.r += self.v
        self.v += self.a
        if v_horizontal > speed_limit_max:
            self.v.x *= speed_limit_max / v_horizontal
            self.v.y *= speed_limit_max / v_horizontal
        if abs(self.v.x) <= speed_limit_min:
            self.v.x = 0
        if abs(self.v.y) <= speed_limit_min:
            self.v.y = 0

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.control_keys:
                self.pressed_keys.append(event.key)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_SPACE:
                self.r.z -= 1
            if event.key == pygame.K_z:
                self.r.z += 1
        elif event.type == pygame.KEYUP:
            if event.key in self.control_keys:
                self.pressed_keys.remove(event.key)
        elif event.type == pygame.MOUSEMOTION:
            mx, my = pygame.mouse.get_pos()
            # x = - delta <= ось с пайгеймой не сходится
            x, y = -k * (mx - int(WIDTH / 2)), k * (my - int(HEIGHT / 2))
            pygame.mouse.set_pos([int(WIDTH / 2), int(HEIGHT / 2)])
            self.vector.an_xy = (x + self.vector.an_xy + pi) % (pi * 2) - pi
            self.vector.an_xz = (y + self.vector.an_xz)
            if self.vector.an_xz > pi / 2:
                self.vector.an_xz = pi / 2
            if self.vector.an_xz < -pi / 2:
                self.vector.an_xz = -pi / 2


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
