import pygame
from graph import Vector
from graph import vector_boosted
from graph.cube_func import draw_cube_func
from scene import Scene
from vocabulary import GREY1, WIDTH, HEIGHT, cut, ground, WHITE, mult, BLACK
import order_of_output


def draw_bottom(screen, cam):
    for i in range(0, order_of_output.distance + 15, 3):
        for j in range(0, order_of_output.distance + 15, 3):
            x_ground, y_ground, condition = vector_boosted.from_world_to_screen(
                int(cam.x) - (order_of_output.distance + 15) / 2 + i,
                int(cam.y) - (order_of_output.distance + 15) / 2 + j, ground + 0.5,
                cam.x, cam.y, cam.z, cam.d, cam.trigonometry_array)
            if condition:
                pygame.draw.circle(screen, (30, 30, 30), (int(x_ground), int(y_ground)), 3)


class Rasterizer:
    def __init__(self):
        self.coord_history = (0, 0, 0)
        self.temp_order = []

    def draw(self, screen: pygame.Surface, scene: Scene, camera: Vector, cub_h=1, ):
        screen.fill(GREY1)
        if self.coord_history != (camera.x, camera.y, camera.z):
            self.coord_history = (camera.x, camera.y, camera.z)
            self.temp_order = cut(scene, order_of_output.order, camera, order_of_output.distance, order_of_output.h_dis)
        fatline = self.selected_block(camera, scene)
        draw_bottom(screen, camera)
        outline = 1
        if type(fatline) == type((1, 2, 3)):
            if fatline[3]:
                outline = 3
                draw_cube_func(screen, scene.map[fatline[0]][fatline[1]][fatline[2]], fatline[0], fatline[1],
                               fatline[2], camera.x, camera.y, camera.z, camera.d, cub_h, camera.trigonometry_array,
                               outline, grnd=fatline[3])
                outline = 1
        for item in self.temp_order:
            if type(fatline) == type((1, 2, 3)):
                if fatline[:-1] == item:
                    outline = 3
            draw_cube_func(screen, scene.map[item[0]][item[1]][item[2]], *item, camera.x, camera.y, camera.z, camera.d,
                           cub_h,
                           camera.trigonometry_array, outline)
            outline = 1

    def selected_block(self, cam, scene):
        rx = cam.x
        ry = cam.y
        rz = cam.z
        for i in range(6 * 7):
            rx += cam.dx / 7 / cam.d
            ry += cam.dy / 7 / cam.d
            rz += cam.dz / 7 / cam.d
            if scene.map[round(rx)][round(ry)][round(rz)]:
                return round(rx), round(ry), round(rz), False
            if round(rz) == ground:
                return round(rx), round(ry), round(rz), True


if __name__ == "__main__":
    print("This module is not for direct call!")
