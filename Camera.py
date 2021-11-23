from vocabulary import *
from graph import *


class Camera(Vector):
    def __init__(self, v0=0, axy=0, g=gravity, h=1.75):
        super(Camera, self).__init__()
        self.vx, self.vy, self.vz = v0, v0, v0
        self.ax, self.ay, self.az = axy, axy, g
        self.h = h
        self.controlling = [0, 0, 0, 0, 0]
        #LEFT, RIGHT, BACKWARD, FORWARD, ROTATE

    def control(self, order, an_xz=0, an_xy=0):
        """
        Механика движения камеры.
        :param order: "приказ" - описание действия. Массив bool'ов [FORWARD, LEFT, BACKWARD, RIGHT, ROTATE]
        :param an_xz: угол в вертикальной плоскости (нужно уточнить направление)
        :param an_xy: угол в горизонтальной плоскости
        :return: ---
        """
        # Матрица повороооота:
        # self.vx = vx * cos(an_xy) - vy * sin(an_xy)
        # self.vy = vx * sin(an_xy) + vy * cos(an_xy)

        for i in range(3):
            if order[i]:
                self.ax += znak[i] * 0.5 * cos(self.an_xy)
                self.ay += znak[i + 1] * 0.5 * sin(self.an_xy)
        if order[0] and order[1] and order[2] and order[3] and (self.vx ** 2 + self.vy ** 2) ** 0.5 > 0.5:
            self.ax = - sign(self.vx) * stopper_acceleration
            self.ay = - sign(self.vy) * stopper_acceleration
        if order[4]:
            self.an_xy = (an_xy + self.an_xy) % pi
            self.an_xz = (an_xz + self.an_xz) % pi
        if self.vx > speed_limit:
            self.vx = speed_limit
        if self.vy > speed_limit:
            self.vy = speed_limit

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        self.vx += self.ax
        self.vy += self.ay
        self.vz += self.az


def coords(screen, cam):
    text_render(screen, "x = " + str(cam.x), 50, 50)
    text_render(screen, "y = " + str(cam.y), 50, 100)
    text_render(screen, "z = " + str(cam.z), 50, 150)
    text_render(screen, "vx = " + str(cam.vx), 50, 200)
    text_render(screen, "vy = " + str(cam.vy), 50, 250)
    text_render(screen, "vz = " + str(cam.vz), 50, 300)
    text_render(screen, "an_xy = " + str(cam.an_xy), 50, 350)
    text_render(screen, "an_xz = " + str(cam.an_xz), 50, 400)


# Обработка действий на нажатие кнопки
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
        x, y = - k * (x - int(WIDTH / 2)), k * (y - int(HEIGHT / 2))  # x = - delta <= ось с пайгейиои не сходится
        pygame.mouse.set_pos([int(WIDTH / 2), int(HEIGHT / 2)])
        return ROTATE, x, y
    else:
        return NOTHING, 0, 0