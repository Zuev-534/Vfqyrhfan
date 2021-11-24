from vocabulary import *
from graph import *


class Camera(Vector):
    def __init__(self, vx0=0, vy0=0, vz0=0, ax=0, ay=0, g=gravity, h=1.75):
        super(Camera, self).__init__()
        self.vx, self.vy, self.vz = vx0, vy0, vz0
        self.ax, self.ay, self.az = ax, ay, g
        self.h = h
        self.d = 10
        self.controlling = [0, 0, 0, 0, 0, 0, 0]
        # LEFT, RIGHT, BACKWARD, FORWARD, ROTATE, an_xy, an_zx

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
        self.ax, self.ay, self.az = 0, 0, 0
        if abs(self.vy) > speed_limit_min:
            self.ay = - sign(self.vy) * stopper_acceleration
        else:
            self.ay = 0
        if abs(self.vx) > speed_limit_min:
            self.ax = - sign(self.vx) * stopper_acceleration
        else:
            self.ax = 0
        if self.controlling[0]:
            self.ax += leg_force * sin(self.an_xy)
            self.ay += -leg_force * cos(self.an_xy)
        if self.controlling[1]:
            self.ax += -leg_force * sin(self.an_xy)
            self.ay += leg_force * cos(self.an_xy)
        if self.controlling[3]:
            self.ax += leg_force * cos(self.an_xy)
            self.ay += leg_force * sin(self.an_xy)
        if self.controlling[2]:
            self.ax += -leg_force * cos(self.an_xy)
            self.ay += -leg_force * sin(self.an_xy)

        if self.controlling[4]:
            self.an_xy = (self.controlling[5] + self.an_xy + pi) % (pi * 2) - pi
            self.an_xz = (self.controlling[6] + self.an_xz)
            if self.an_xz > pi / 2:
                self.an_xz = pi / 2
            if self.an_xz < -pi / 2:
                self.an_xz = -pi / 2
            self.controlling[4], self.controlling[5], self.controlling[6] = 1, 0, 0

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        self.vx += self.ax
        self.vy += self.ay
        self.vz += self.az
        if sqrt(self.vx**2 +self.vy**2) > speed_limit_max:
            self.vx *= speed_limit_max / sqrt(self.vx**2 +self.vy**2)
            self.vy *= speed_limit_max / sqrt(self.vx**2 +self.vy**2)
        if abs(self.vx) <= speed_limit_min:
            self.vx = 0
        if abs(self.vy) <= speed_limit_min:
            self.vy = 0

    def interoperate(self, input_movement):
        # LEFT, RIGHT, BACKWARD, FORWARD, ROTATE, an_xy, an_xz - controlling
        if input_movement.type == pygame.QUIT:
            pygame.quit()
        elif input_movement.type == pygame.KEYDOWN:
            if input_movement.key == pygame.K_ESCAPE:
                pygame.quit()
            elif input_movement.key == pygame.K_d:
                self.controlling[0] = 1
            elif input_movement.key == pygame.K_a:
                self.controlling[1] = 1
            elif input_movement.key == pygame.K_s:
                self.controlling[2] = 1
            elif input_movement.key == pygame.K_w:
                self.controlling[3] = 1
        elif input_movement.type == pygame.KEYUP:
            if input_movement.key == pygame.K_d:
                self.controlling[0] = 0
            elif input_movement.key == pygame.K_a:
                self.controlling[1] = 0
            elif input_movement.key == pygame.K_s:
                self.controlling[2] = 0
            elif input_movement.key == pygame.K_w:
                self.controlling[3] = 0
        elif input_movement.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            x, y = - k * (x - int(WIDTH / 2)), k * (y - int(HEIGHT / 2))  # x = - delta <= ось с пайгейиои не сходится
            pygame.mouse.set_pos([int(WIDTH / 2), int(HEIGHT / 2)])
            self.controlling[4], self.controlling[5], self.controlling[6] = 1, x, y


def coords(screen, cam):
    text_render(screen, "x = " + str(cam.x)[:4], 50, 30)
    text_render(screen, "y = " + str(cam.y)[:4], 50, 60)
    text_render(screen, "z = " + str(cam.z)[:4], 50, 90)
    text_render(screen, "vx = " + str(cam.vx)[:4], 50, 120)
    text_render(screen, "vy = " + str(cam.vy)[:4], 50, 150)
    text_render(screen, "vz = " + str(cam.vz)[:4], 50, 180)
    text_render(screen, "ax = " + str(cam.ax)[:4], 50, 210)
    text_render(screen, "ay = " + str(cam.ay)[:4], 50, 240)
    text_render(screen, "az = " + str(cam.az)[:4], 50, 270)
    text_render(screen, "an_xy = " + str(cam.an_xy)[:4], 50, 300)
    text_render(screen, "an_xz = " + str(cam.an_xz)[:4], 50, 330)
    text_render(screen, str(cam.controlling), 50, 360)
