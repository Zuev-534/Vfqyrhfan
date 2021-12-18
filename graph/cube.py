from graph.vector import Vector
from vocabulary import GREEN, BLACK
from pygame.draw import polygon


class Cube:
    def __init__(self, x0=0, y0=0, z0=0, color=GREEN, h0=1, vis=1):
        self.x = x0
        self.y = y0
        self.z = z0
        self.color = color
        self.h = h0
        self.points = None
        self.coords_2d = [[[(0, 0) for j in range(2)] for i in range(2)] for k in range(2)]

        self.vizible = vis
        self.main = Vector(x0, y0, z0)

        self.set_coords_with_move()

    def set_coords_with_move(self):
        self.points = [[[Vector(0, 0, 0) for j in range(2)] for i in range(2)] for k in range(2)]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    self.points[i][j][k].x = self.x + (-1) ** (i + 1) * self.h / 2
                    self.points[i][j][k].y = self.y + (-1) ** (j + 1) * self.h / 2
                    self.points[i][j][k].z = self.z + (-1) ** (k + 1) * self.h / 2

    def print_all(self):
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    print(self.points[i][j][k].x)
                    print(self.points[i][j][k].y)
                    print(self.points[i][j][k].z)

    def cub_are_vis_or(self, cam):
        global counter
        self.main.new_di_in_new_pos(cam)
        self.main.set_coords_d_from_di()
        # if self.main.get_angle_cos(cam) > 1 / 2:
        #     self.vizible = 1
        # else:
        #     self.vizible = 0

    def draw_cube(self, screen, cam: Vector):
        self.cub_are_vis_or(cam)
        if self.vizible == 1:

            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        x, y = self.points[i][j][k].get_vector(cam).coords_to_cam(cam)
                        self.coords_2d[i][j][k] = (x, y)

            if cam.x > self.x + self.h / 2:
                self.draw_square(screen, cam, i=3)
            elif cam.x < self.x - self.h / 2:
                self.draw_square(screen, cam, i=2)
            if cam.y > self.y + self.h / 2:
                self.draw_square(screen, cam, j=3)
            elif cam.y < self.y - self.h / 2:
                self.draw_square(screen, cam, j=2)
            if cam.z > self.z + self.h / 2:
                self.draw_square(screen, cam, k=3)
            elif cam.z < self.z - self.h / 2:
                self.draw_square(screen, cam, k=2)
        else:
            pass

    def draw_square(self, screen, cam, i=0, j=0, k=0):
        if i == 2 or i == 3:
            polygon(screen, self.color,
                    [self.coords_2d[i - 2][0][0],
                     self.coords_2d[i - 2][0][1],
                     self.coords_2d[i - 2][1][1],
                     self.coords_2d[i - 2][1][0]])
            polygon(screen, BLACK,
                    [self.coords_2d[i - 2][0][0],
                     self.coords_2d[i - 2][0][1],
                     self.coords_2d[i - 2][1][1],
                     self.coords_2d[i - 2][1][0]], 1)

        if j == 2 or j == 3:
            polygon(screen, self.color,
                    [self.coords_2d[0][j - 2][0],
                     self.coords_2d[0][j - 2][1],
                     self.coords_2d[1][j - 2][1],
                     self.coords_2d[1][j - 2][0]])
            polygon(screen, BLACK,
                    [self.coords_2d[0][j - 2][0],
                     self.coords_2d[0][j - 2][1],
                     self.coords_2d[1][j - 2][1],
                     self.coords_2d[1][j - 2][0]], 1)

        if k == 2 or k == 3:
            polygon(screen, self.color,
                    [self.coords_2d[0][0][k - 2],
                     self.coords_2d[0][1][k - 2],
                     self.coords_2d[1][1][k - 2],
                     self.coords_2d[1][0][k - 2]])
            polygon(screen, BLACK,
                    [self.coords_2d[0][0][k - 2],
                     self.coords_2d[0][1][k - 2],
                     self.coords_2d[1][1][k - 2],
                     self.coords_2d[1][0][k - 2]], 1)


if __name__ == "__main__":
    print("This module is not for direct call!")
