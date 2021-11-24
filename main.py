from vocabulary import *
from Camera import *

Victor = Camera()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Test controlling')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
Victor.x, Victor.y = 90, 90
u = 15
cub = Cube(3, 3, 3)
cub.set_coords_with_move()
while True:
    clock.tick(FPS)
    screen.fill(GREY1)
    for event in pygame.event.get():
        Victor.interoperate(event)
        Victor.control()
    Victor.move()
    coords(screen, Victor)
    circle(screen, BLACK, (Victor.x, Victor.y), 5)
    circle(screen, BLACK, (10, 100), 5)
    circle(screen, BLACK, (100, 111), 5)

    circle(screen, BLACK, Vector(10, 100, 0).get_vector(Victor).coords_to_cam(Victor), 10)
    pygame.draw.lines(screen, WHITE, True,
                      [(Victor.x, Victor.y), (Victor.x + u * cos(Victor.an_xy), Victor.y + u * sin(Victor.an_xy))], 2)
    circle(screen, BLACK, Vector(100, 111, 2000000).get_vector(Victor).coords_to_cam(Victor), 10)
    cub.draw_cube(screen, Victor)
    pygame.display.update()
