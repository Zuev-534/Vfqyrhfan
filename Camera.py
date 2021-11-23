from vocabulary import *
from graph import *

class Camera(Vector):
    def __init__(self, v0 = 0, h=1.75):
        super(Camera, self).__init__()
        self.vx = v0
        self.vy = v0
        self.h = h

    def control(self, order, an_xz = 0, an_xy = 0):
        """
        Механика движения камеры.
        :param order: "приказ" - описание действия.
        :param an_xz: угол в вертикальной плоскости (нужно уточнить направление)
        :param an_xy: угол в горизонтальной плоскости
        :return: ---
        """
        # Матрица повороооота:
        # self.vx = vx * cos(an_xy) - vy * sin(an_xy)
        # self.vy = vx * sin(an_xy) + vy * cos(an_xy)
        self.vx = int(int(0.4 * self.vx*100)/100)
        self.vy = int(int(0.4 * self.vy*100)/100)
        if order == NOTHING:
            pass
        if order == ROTATE:
            self.an_xy = (an_xy + self.an_xy) % pi
            self.an_xz = (an_xz + self.an_xz) % pi
        if order == LEFT:
            self.vx += 5 * sin(self.an_xy)
            self.vy += -5 * cos(self.an_xy)
        if order == RIGHT:
            self.vx += -5 * sin(self.an_xy)
            self.vy += 5 * cos(self.an_xy)
        if order == FORWARD:
            self.vx += 5 * cos(self.an_xy)
            self.vy += 5 * sin(self.an_xy)
        if order == BACKWARD:
            self.vx += -5 * cos(self.an_xy)
            self.vy += -5 * sin(self.an_xy)
    def move(self):
        self.x += self.vx
        self.y += self.vy

def coords(screen, cam):
    text_render(screen, "x = " + str(cam.x), 50, 50)
    text_render(screen, "y = " + str(cam.y), 50, 100)
    text_render(screen, "an_xy = " + str(cam.an_xy), 50, 150)
    text_render(screen, "an_xz = " + str(cam.an_xz), 50, 200)



def interoperate(input_movement):
    if input_movement.type == pygame.QUIT:
        pygame.quit()
    elif input_movement.type == pygame.KEYDOWN:
        if input_movement.key == pygame.K_ESCAPE:
            pygame.quit()
    if input_movement.type == pygame.MOUSEMOTION:
        x, y = pygame.mouse.get_pos()
        x, y = - k * (x - int(WIDTH / 2)), k * (y - int(HEIGHT / 2)) # x = - delta <= ось с пайгейиои не сходится
        pygame.mouse.set_pos([int(WIDTH / 2), int(HEIGHT / 2)])
        return ROTATE, x, y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        return FORWARD, 0, 0
    elif keys[pygame.K_s]:
        return BACKWARD, 0, 0
    elif keys[pygame.K_a]:
        return LEFT, 0, 0
    elif keys[pygame.K_d]:
        return RIGHT, 0, 0
    return NOTHING, 0, 0













# # Обработка действий на нажатие кнопки
# def interoperate(input_movement):
#     if input_movement.type == pygame.QUIT:
#         pygame.quit()
#     elif input_movement.type == pygame.KEYDOWN:
#         if input_movement.key == pygame.K_ESCAPE:
#             pygame.quit()
#         elif input_movement.key == pygame.K_a:
#             return LEFT, 0, 0
#         elif input_movement.key == pygame.K_d:
#             return RIGHT, 0, 0
#         elif input_movement.key == pygame.K_s:
#             return BACKWARD, 0, 0
#         elif input_movement.key == pygame.K_w:
#             return FORWARD, 0, 0
#     elif input_movement.type == pygame.MOUSEMOTION:
#         x, y = pygame.mouse.get_pos()
#         x, y = - k * (x - int(WIDTH / 2)), k * (y - int(HEIGHT / 2)) # x = - delta <= ось с пайгейиои не сходится
#         pygame.mouse.set_pos([int(WIDTH / 2), int(HEIGHT / 2)])
#         return ROTATE, x, y
#     else:
#         return NOTHING, 0, 0
