from vocabulary import *
from player import Player, coords
from graph.cube import Cube
from graph.vector import Vector
import time

victor = Player()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Test controlling')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
victor.x, victor.y = 9, 9

u = 15
cubs = [[Cube(15+4*i, 3 + 5 * j, 3) for i in range(20)]for j in range(30)]
cubs1 = [[Cube(15+4*i, 3 + 5 * j, 8) for i in range(20)]for j in range(30)]
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
        victor.interoperate(event)
    victor.control()
    victor.move()

    circle(screen, BLACK, convert_point((victor.x, victor.y, 0), mm_o), 5)
    circle(screen, BLACK, convert_point((10, 100, 0), mm_o), 5)
    circle(screen, BLACK, convert_point((100, 111, 0), mm_o), 5)

    circle(screen, BLACK, Vector(10, 100, 0).get_vector(victor).coords_to_cam(victor), 10)

    pygame.draw.lines(screen, WHITE, True,
                      [convert_point((victor.x, victor.y, 0), mm_o),
                       convert_point((victor.x + u * cos(victor.an_xy), victor.y + u * sin(victor.an_xy), 0), mm_o)], 2)
    circle(screen, BLACK, Vector(100, 111, 2000000).get_vector(victor).coords_to_cam(victor), 10)
    for cub in cubs1:
        for a in cub:
            a.draw_cube(screen, victor)
    for cub in cubs:
        for a in cub:
            a.draw_cube(screen, victor)

    coords(screen, victor, 1.0 / (time.time() - start_time))
    pygame.display.update()