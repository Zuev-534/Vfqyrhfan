from vocabulary import *
from player import Player, coords
from graph.cube import Cube
from graph.vector import Vector
import pygame
import time

victor = Player(pygame.Vector3(9, 9, 0), gravity)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Test controlling')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

u = 15
cubs = [[Cube(15 + 4 * i, 3 + 5 * j, 3) for i in range(20)] for j in range(30)]
cubs1 = [[Cube(15 + 4 * i, 3 + 5 * j, 8) for i in range(20)] for j in range(30)]
for i in cubs:
    for t in i:
        t.set_coords_with_move()
for i in cubs1:
    for t in i:
        t.set_coords_with_move()

while True:
    start_time = time.time()  # start time of the loop
    clock.tick(FPS)
    screen.fill(GREY1)
    for event in pygame.event.get():
        victor.update(event)
    victor.move()

    circle(screen, BLACK, convert_point((victor.vector.x, victor.vector.y, 0), mm_o), 5)
    circle(screen, BLACK, convert_point((10, 100, 0), mm_o), 5)
    circle(screen, BLACK, convert_point((100, 111, 0), mm_o), 5)

    circle(screen, BLACK, Vector(10, 100, 0).get_vector(victor.get_camera()).coords_to_cam(victor.get_camera()), 10)

    pygame.draw.lines(screen, WHITE, True, [
        convert_point((victor.vector.x, victor.vector.y, 0), mm_o),
        convert_point((
            victor.vector.x + u * cos(victor.vector.an_xy),
            victor.vector.y + u * sin(victor.vector.an_xy),
            0,
        ), mm_o),
    ], 2)
    circle(screen, BLACK, Vector(100, 111, 2000000).get_vector(victor.get_camera()).coords_to_cam(victor.get_camera()), 10)
    for cub in cubs1:
        for a in cub:
            a.draw_cube(screen, victor.get_camera())
    for cub in cubs:
        for a in cub:
            a.draw_cube(screen, victor.get_camera())

    coords(screen, victor, 1.0 / (time.time() - start_time))
    pygame.display.update()
