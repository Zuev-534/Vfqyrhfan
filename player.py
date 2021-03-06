from vocabulary import *
import graph
from graph import Vector
import pygame


class Player:
    def __init__(self, point: tuple([float, float, float]), g: float, screen_size: tuple([int, int])):
        """
        инициализирует игрока,
        # longitude - долгота угла
        # latitude - широта угла
        points: начальное положение
        g: ускорение свободного падения
        screen_size: размер экрана
        """
        self.r = pygame.Vector3(point)
        self.v = pygame.Vector3()
        self.a = pygame.Vector3()
        self.lng = 0  # longitude
        self.lat = 0  # latitude
        self.g = g
        self.test_mode = False
        self.n = 8
        self.cam = None

        self.control_keys = [pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_SPACE]
        self.pressed_keys = []
        self.fly_mode = True

        self.screen_size = screen_size
        self.color = 4

    def get_camera(self) -> Vector:
        """
        return: возвращает вектор евклидовых координат из полярных координат
        """
        self.cam = Vector.from_polar(self.r.x, self.r.y, self.r.z, self.lng, self.lat, 0.1)
        return self.cam

    def update(self, event, scene, fat):
        """
        обновляет конфигурацию нажатых клавиш и перемещает угол взгляда игрока посредством измерения перемещения мыши,
        отвечает за обработку событий и распределяет задачи между методами по обработке событий
        event: пайгеймовское событие
        scene: хранит массив блоков и их цвета
        fat: хранит информацию о выделенном кубе
        return: True, если игрок поставил/убрал куб
        """
        const = False
        if event.type == pygame.KEYDOWN:
            if event.key in self.control_keys:
                self.pressed_keys.append(event.key)
            if event.key == pygame.K_c:
                self.fly_mode = not self.fly_mode
            elif event.key == pygame.K_t:
                self.test_mode = not self.test_mode
            elif event.key == pygame.K_SPACE and not self.fly_mode:
                self.jump()
            elif event.key == pygame.K_m:
                music()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                scene.dest_block(fat)
                const = True
            if event.button == 3:
                scene.add_block(fat, self.color)
                const = True
            if event.button == 4:
                self.change_color(1)
            if event.button == 5:
                self.change_color(-1)
        elif event.type == pygame.KEYUP:
            if event.key in self.control_keys:
                self.pressed_keys.remove(event.key)
        elif event.type == pygame.MOUSEMOTION:
            mx, my = pygame.mouse.get_pos()
            # x = - delta <= ось с пайгеймой не сходится
            w, h = self.screen_size
            x, y = -k * (mx - w // 2), k * (my - h // 2)
            pygame.mouse.set_pos([w // 2, h // 2])
            self.lng = (self.lng + x + np.pi) % (np.pi * 2) - np.pi
            self.lat = (self.lat - y)
            if self.lat > np.pi / 2:
                self.lat = np.pi / 2
            if self.lat < -np.pi / 2:
                self.lat = -np.pi / 2
        elif event.type == pygame.VIDEORESIZE:
            self.screen_size = (event.w, event.h)
        return const

    def move(self, order, ground, scene):
        """
        перемещает игрока посредством добавления вектору скорости ускорения, замедляет его при слишком большой скорости.
        order: соседние блоки в относительных координатах
        ground: уровень земли в мире
        scene: хранит массив блоков и их цвета
        return: None
        """
        v_horizontal = np.sqrt(self.v.x ** 2 + self.v.y ** 2)
        if v_horizontal > speed_limit_min:
            self.a.y = -self.v.y / v_horizontal * stopper_acceleration
            self.a.x = -self.v.x / v_horizontal * stopper_acceleration
        else:
            self.a.x = 0
            self.a.y = 0
        if abs(self.v.z) > speed_limit_min:
            self.a.z = - sign(self.v.z) * stopper_acceleration * 2
        else:
            self.a.z = 0

        for key in self.pressed_keys:
            if key == pygame.K_d:
                self.a.x += +leg_force * np.sin(self.lng)
                self.a.y += -leg_force * np.cos(self.lng)
            elif key == pygame.K_a:
                self.a.x += -leg_force * np.sin(self.lng)
                self.a.y += +leg_force * np.cos(self.lng)
            elif key == pygame.K_s:
                self.a.x += -leg_force * np.cos(self.lng)
                self.a.y += -leg_force * np.sin(self.lng)
            elif key == pygame.K_w:
                self.a.x += +leg_force * np.cos(self.lng)
                self.a.y += +leg_force * np.sin(self.lng)
            elif key == pygame.K_SPACE and self.fly_mode:
                if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                    self.a.z += -leg_force
                else:
                    self.a.z += +leg_force
        if not self.fly_mode:
            self.a.z = self.g

        if v_horizontal > speed_limit_max:
            self.v.x *= speed_limit_max / v_horizontal
            self.v.y *= speed_limit_max / v_horizontal
        if abs(self.v.z) > speed_limit_max and self.fly_mode:
            self.v.z *= speed_limit_max / abs(self.v.z)
        if abs(self.v.z) > 3 * speed_limit_max and not self.fly_mode:
            self.v.z *= 3 * speed_limit_max / abs(self.v.z)
        if abs(self.v.x) <= speed_limit_min:
            self.v.x = 0
        if abs(self.v.y) <= speed_limit_min:
            self.v.y = 0
        if abs(self.v.z) <= speed_limit_min:
            self.v.z = 0

        self.check_tuk(order, ground, scene)
        self.r += self.v
        self.v += self.a

    def check_tuk(self, order, ground, scene):
        """
        Проверяет нахождение поблизости блоков и изменяет вектор скорости для того, чтобы нельзя было к ним приближаться
        order: соседние блоки в относительных координатах
        ground: уровень земли в мире
        scene: хранит массив блоков и их цвета
        return: None
        """
        ret = graph.vector.check_distance(scene, self.cam, order, ground)
        if ret[0] and self.v.x >= 0:
            self.v.x = 0
            self.r.x -= 0.001
        if ret[1] and self.v.y >= 0:
            self.v.y = 0
            self.r.y -= 0.001
        if ret[2] and self.v.z >= 0:
            self.v.z = 0
            self.r.z -= 0.001
        if ret[3] and self.v.x <= 0:
            self.v.x = 0
            self.r.x += 0.001
        if ret[4] and self.v.y <= 0:
            self.v.y = 0
            self.r.y += 0.001
        if ret[5] and self.v.z <= 0:
            self.v.z = 0
            self.r.z += 0.001

    def jump(self):
        """
        добавляет вектор скорости вверх при нулевой вертикальной компоненте скорости
        return: None
        """
        if abs(abs(self.v.z) - 0.003) < 0.0000001:
            self.v.z = speed_limit_max * 1.5

    def change_color(self, rotate):
        """
        изменяет цвет в соответствии с поворотом колёсика мыши
        rotate: направление поворота колёсика (1- вперёд, -1 - назад)
        return: None
        """
        if rotate > 0:
            self.color += 1
        elif rotate < 0:
            self.color -= 1
        if self.color == 9:
            self.color = 1
        elif self.color == 0:
            self.color = 8


def coords(screen, player: Player, fps):
    """
    отладочная функция, выводит на экран основные переменные отвечающие за положение и перемещение
    return: None
    """
    if player.test_mode:
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
        text_render(screen, "fly_mode = " + str(player.fly_mode)[:4], 50, 360)


if __name__ == "__main__":
    print("This module is not for direct call!")
