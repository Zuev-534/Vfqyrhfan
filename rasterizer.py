import numpy as np
import pygame
from graph import Vector
from graph import vector_boosted
from graph.cube_func import draw_cube_func
from scene import Scene
from vocabulary import GREY1, cut, ground, get_color
import order_of_output


class Rasterizer:
    def __init__(self):
        self.coord_history = (0, 0, 0)
        self.temp_order = []
        self.fat = None
        self.player_const = 0

    def draw(self, screen: pygame.Surface, scene: Scene, camera: Vector, cub_h=1):
        """
        распределяет задачи по отрисовке между draw_bottom и draw_cubes
        screen:пайгеймовский экран, на который надо отрисовывать
        scene:в ней хранятся данные о положении и цвете кубов
        camera:камера
        cub_h: размер кубов(лучше не менять)
        return:None
        """
        screen.fill(GREY1)
        self.draw_bottom(screen, camera)
        self.draw_cubes(screen, scene, camera, cub_h)

    def draw_cubes(self, screen: pygame.Surface, scene: Scene, camera: Vector, const, cub_h=1):
        """
        отвечает за отрисовку кубов, за само выделение блоков,
        внутри себя создаёт порядок отрисовки и по нему рисует кубы,
        обновляет карту при взаимодействии игрока с объектами
        screen: пайгеймовский экран, на который надо отрисовывать
        scene: в ней хранятся данные о положении и цвете кубов
        camera: камера
        const:True если требуется обновление карты в следствии взаимодействия игрока с объектами
        cub_h: размер кубов(лучше не менять)
        return:None
        """
        if self.coord_history != (camera.x, camera.y, camera.z) or const:
            self.player_const = 0
            self.coord_history = (camera.x, camera.y, camera.z)
            self.temp_order = cut(scene, order_of_output.order, camera, order_of_output.distance, order_of_output.h_dis)
        self.fat = self.selected_block(camera, scene)
        self.draw_bottom(screen, camera)
        outline = 1
        if isinstance(self.fat, tuple):
            if self.fat[3]:
                outline = 3
                draw_cube_func(screen, scene.map[self.fat[0]][self.fat[1]][self.fat[2]], self.fat[0],
                               self.fat[1],
                               self.fat[2], camera.x, camera.y, camera.z, camera.d, cub_h,
                               camera.trigonometry_array,
                               outline, grnd=self.fat[3])
                outline = 1
        for item in self.temp_order:
            if isinstance(self.fat, tuple):
                if self.fat[:-2] == item:
                    outline = 3
            draw_cube_func(screen, scene.map[item[0]][item[1]][item[2]], *item, camera.x, camera.y, camera.z, camera.d,
                           cub_h,
                           camera.trigonometry_array, outline)
            outline = 1

    @staticmethod
    def draw_bottom(screen: pygame.Surface, camera: Vector):
        """
        отвечает за отрисовку нижней границы мира
        screen: экран из пайгейма
        camera: камера
        return: None
        """
        border = np.zeros(((order_of_output.distance + 2) // 3 + 1, (order_of_output.distance + 2) // 3 + 1, 2),
                          dtype='int')
        for i in range(0, order_of_output.distance + 2, 3):
            for j in range(0, order_of_output.distance + 2, 3):
                x_ground, y_ground, condition = vector_boosted.from_world_to_screen(
                    int(camera.x) + 0.5 - (order_of_output.distance + 2) / 2 + i,
                    int(camera.y) + 0.5 - (order_of_output.distance + 2) / 2 + j, ground + 0.5,
                    camera.x, camera.y, camera.z, camera.d, camera.trigonometry_array, screen.get_clip().size)
                if condition:
                    border[i // 3][j // 3][0], border[i // 3][j // 3][1] = int(x_ground), int(y_ground)

        bottom = np.zeros(((order_of_output.distance + 2) // 3 * 3 * 4 - 4, 2))

        c = 0
        # х - отрицательный
        a = 0
        for j in range(0, order_of_output.distance + 2, 3):
            if border[a // 3][j // 3][0] != 0 and border[a // 3][j // 3][0] != 0:
                bottom[c] = border[a // 3][j // 3]
                c += 1
        # у- положителььный
        a = (order_of_output.distance + 2) // 3 * 3
        for i in range(0, order_of_output.distance + 2, 3):
            if border[i // 3][a // 3][0] != 0 and border[i // 3][a // 3][0] != 0:
                bottom[c] = border[i // 3][a // 3]
                c += 1
        # х - положительный
        a = (order_of_output.distance + 2) // 3 * 3
        for j in range((order_of_output.distance + 2) // 3 * 3, -1, -3):
            if border[a // 3][j // 3][0] != 0 and border[a // 3][j // 3][0] != 0:
                bottom[c] = border[a // 3][j // 3]
                c += 1
        # y - отрицательный
        for i in range((order_of_output.distance + 2) // 3 * 3, -1, -3):
            if border[i // 3][0 // 3][0] != 0 and border[i // 3][0 // 3][0] != 0:
                bottom[c] = border[i // 3][0 // 3]
                c += 1
        bottom = bottom[~np.all(bottom == 0, axis=1)]
        array = (bottom.tolist())
        array.sort()
        c = 0
        W, H = screen.get_clip().size
        while c <= len(array)-1:
            if array[c][1] >= H:
                del array[c]
            else:
                c += 1

        if array[0][0] < 0 or 0 < array[0][1] < H and array[-1][0] > W or 0 < array[-1][1] < H:
            pygame.draw.polygon(screen, get_color(0), [[0, H], *array, [W, H]])
        else:
            pygame.draw.polygon(screen, get_color(0), array)

    @staticmethod
    def selected_block(cam, scene):
        """
        получает на вход камеру и массив кубов, выдаёт координату куба который требуется выделить
        и сторону куба на который наводится игрок
        cam: камера
        scene: массив блоков
        return: координаты в формате x, y, z True/False в зависимости от того выделен куб или пол,
        сторону в формате какую координату надо добавить или убавить
        """
        rx = cam.x
        ry = cam.y
        rz = cam.z
        for _ in range(6 * 10):
            rx += cam.dx / 10 / cam.d
            ry += cam.dy / 10 / cam.d
            rz += cam.dz / 10 / cam.d
            k = [0 for _ in range(3)]
            if scene.map[round(rx)][round(ry)][round(rz)]:

                a = round(rx)
                b = round(ry)
                c = round(rz)
                a_0 = abs(rx - round(rx))
                b_0 = abs(ry - round(ry))
                c_0 = abs(rz - round(rz))
                maximum = max(abs(rx - round(rx)), abs(ry - round(ry)), abs(rz - round(rz)))

                if maximum == a_0:
                    if rx - round(rx) <= 0:
                        k[0] = -1
                    else:
                        k[0] = 1
                elif maximum == b_0:
                    if ry - round(ry) <= 0:
                        k[1] = -1
                    else:
                        k[1] = 1
                elif maximum == c_0:
                    if rz - round(rz) <= 0:
                        k[2] = -1
                    else:
                        k[2] = 1

                return a, b, c, False, k
            if round(rz) == ground:
                k[2] = 1
                return round(rx), round(ry), round(rz), True, k


if __name__ == "__main__":
    print("This module is not for direct call!")
