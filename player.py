from vocabulary import *
from graph import Vector
import pygame


class Player:
    def __init__(self, r: pygame.Vector3, g: float):
        self.r = r
        self.v = pygame.Vector3()
        self.a = pygame.Vector3(0, 0, g)
        self.h = 1.75
        self.lng = 0 # longitude - долгота угла
        self.lat = 0 # latitude - широта угла

        self.control_keys = [pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d]
        self.pressed_keys = []

    def get_camera(self) -> Vector:
        return Vector.from_polar(self.r.x, self.r.y, self.r.z, self.lng, self.lat, 10)

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
                self.a.x += +leg_force * sin(self.lng)
                self.a.y += -leg_force * cos(self.lng)
            elif key == pygame.K_a:
                self.a.x += -leg_force * sin(self.lng)
                self.a.y += +leg_force * cos(self.lng)
            elif key == pygame.K_s:
                self.a.x += -leg_force * cos(self.lng)
                self.a.y += -leg_force * sin(self.lng)
            elif key == pygame.K_w:
                self.a.x += +leg_force * cos(self.lng)
                self.a.y += +leg_force * sin(self.lng)

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
            self.lng = (x + self.lng + pi) % (pi * 2) - pi
            self.lat = (y + self.lat)
            if self.lat > pi / 2:
                self.lat = pi / 2
            if self.lat < -pi / 2:
                self.lat = -pi / 2


def coords(screen, player: Player, fps):
    text_render(screen, "FPS = " + str(fps)[:4], 50, 10)
    text_render(screen, "x = " + str(player.r.x)[:4], 50, 30)
    text_render(screen, "y = " + str(player.r.y)[:4], 50, 60)
    text_render(screen, "z = " + str(player.r.z)[:4], 50, 90)
    text_render(screen, "vx = " + str(player.v.x * 10)[:4], 50, 120)
    text_render(screen, "vy = " + str(player.v.y * 10)[:4], 50, 150)
    text_render(screen, "vz = " + str(player.v.z * 10)[:4], 50, 180)
    text_render(screen, "ax = " + str(player.a.x * 100)[:4], 50, 210)
    text_render(screen, "ay = " + str(player.a.y * 100)[:4], 50, 240)
    text_render(screen, "az = " + str(player.a.z * 100)[:4], 50, 270)
    text_render(screen, "an_xy = " + str(player.lng)[:4], 50, 300)
    text_render(screen, "an_xz = " + str(player.lat)[:4], 50, 330)
