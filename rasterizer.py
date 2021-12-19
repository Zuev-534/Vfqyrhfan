import pygame
from graph import Vector
from graph import vector_boosted
from graph.cube_func import draw_cube_func
from scene import Scene
from vocabulary import GREY1, cut, ground, WHITE, mult, BLACK
import order_of_output


def draw_bottom(screen: pygame.Surface, cam: Vector):
    for i in range(0, order_of_output.distance + 15, 3):
        for j in range(0, order_of_output.distance + 15, 3):
            x_ground, y_ground, condition = vector_boosted.from_world_to_screen(
                int(cam.x) - (order_of_output.distance + 15) / 2 + i,
                int(cam.y) - (order_of_output.distance + 15) / 2 + j, ground + 0.5,
                cam.x, cam.y, cam.z, cam.d, cam.trigonometry_array, screen.get_clip().size)
            if condition:
                pygame.draw.circle(screen, (30, 30, 30), (int(x_ground), int(y_ground)), 3)


class Rasterizer:
    def __init__(self):
        self.coord_history = (0, 0, 0)
        self.temp_order = []
        self.fatline = None

    def draw(self, screen: pygame.Surface, scene: Scene, camera: Vector, cub_h=1):
        screen.fill(GREY1)
        if self.coord_history != (camera.x, camera.y, camera.z):
            self.coord_history = (camera.x, camera.y, camera.z)
            self.temp_order = cut(scene, order_of_output.order, camera, order_of_output.distance, order_of_output.h_dis)
        self.fatline = self.selected_block(camera, scene)
        draw_bottom(screen, camera)
        outline = 1
        if isinstance(self.fatline, tuple):
            if self.fatline[3]:
                outline = 3
                draw_cube_func(screen, scene.map[self.fatline[0]][self.fatline[1]][self.fatline[2]], self.fatline[0],
                               self.fatline[1],
                               self.fatline[2], camera.x, camera.y, camera.z, camera.d, cub_h,
                               camera.trigonometry_array,
                               outline, grnd=self.fatline[3])
                outline = 1
        for item in self.temp_order:
            if isinstance(self.fatline, tuple):
                if self.fatline[:-2] == item:
                    outline = 3
            draw_cube_func(screen, scene.map[item[0]][item[1]][item[2]], *item, camera.x, camera.y, camera.z, camera.d,
                           cub_h,
                           camera.trigonometry_array, outline)
            outline = 1

    @staticmethod
    def selected_block(cam, scene):
        """
        получает на вход камеру и массив кубов, выдаёт координату куба который требуется выделить
        и сторону куба на который наводится игрок
        cam: камера
        scene: массив блоков
        return: координаты в формате x, y, z True/False в зависимости от того выделен куб или пол,
        сторону в формате 0+x, 1-x, 2+y, 3-y, 4+z, 5-z.
        """
        rx = cam.x
        ry = cam.y
        rz = cam.z
        for _ in range(6 * 7):
            rx += cam.dx / 7 / cam.d
            ry += cam.dy / 7 / cam.d
            rz += cam.dz / 7 / cam.d

            if scene.map[round(rx)][round(ry)][round(rz)]:
                k = 4
                if max(abs(rx - round(rx)), abs(ry - round(ry)), abs(rz - round(rz))) == abs(rx - round(rx)):
                    if rx - round(rx) >= 0:
                        k = 0
                    else:
                        k = 1
                elif max(abs(rx - round(rx)), abs(ry - round(ry)), abs(rz - round(rz))) == abs(ry - round(ry)):
                    if ry - round(ry) >= 0:
                        k = 2
                    else:
                        k = 3
                elif max(abs(rx - round(rx)), abs(ry - round(ry)), abs(rz - round(rz))) == abs(rz - round(rz)):
                    if rz - round(rz) >= 0:
                        k = 4
                    else:
                        k = 5

                return round(rx), round(ry), round(rz), False, k
            if round(rz) == ground:
                return round(rx), round(ry), round(rz), True, 4


if __name__ == "__main__":
    print("This module is not for direct call!")
