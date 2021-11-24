from vocabulary import *
from Camera import *
import time

Victor = Camera()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Test controlling')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
Victor.x, Victor.y = 9, 9

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
        Victor.interoperate(event)
    Victor.control()
    Victor.move()

    circle(screen, BLACK, convert_point((Victor.x, Victor.y, 0), mm_o), 5)
    circle(screen, BLACK, convert_point((10, 100, 0), mm_o), 5)
    circle(screen, BLACK, convert_point((100, 111, 0), mm_o), 5)

    circle(screen, BLACK, Vector(10, 100, 0).get_vector(Victor).coords_to_cam(Victor), 10)
    pygame.draw.lines(screen, WHITE, True,
                      [convert_point((Victor.x, Victor.y, 0), mm_o),
                       convert_point((Victor.x + u * cos(Victor.an_xy), Victor.y + u * sin(Victor.an_xy), 0), mm_o)], 2)
    circle(screen, BLACK, Vector(100, 111, 2000000).get_vector(Victor).coords_to_cam(Victor), 10)
    for cub in cubs:
        for a in cub:
            a.draw_cube(screen, Victor)
    for cub in cubs1:
        for a in cub:
            a.draw_cube(screen, Victor)
    coords(screen, Victor, 1.0 / (time.time() - start_time))
    pygame.display.update()