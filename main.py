from vocabulary import *
from Camera import *

Victor = Camera()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Test controlling')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
Victor.x, Victor.y = 9, 9

u = 15
cub = Cube(3, 3, 3)

while True:
    clock.tick(FPS)
    screen.fill(GREY1)
    for event in pygame.event.get():
        Victor.interoperate(event)
    Victor.control()
    Victor.move()
    coords(screen, Victor)
    circle(screen, BLACK, convert_point((Victor.x, Victor.y, 0), mm_o), 5)
    circle(screen, BLACK, convert_point((10, 100, 0), mm_o), 5)
    circle(screen, BLACK, convert_point((100, 111, 0), mm_o), 5)

    circle(screen, BLACK, Vector(10, 100, 0).get_vector(Victor).coords_to_cam(Victor), 10)
    pygame.draw.lines(screen, WHITE, True,
                      [convert_point((Victor.x, Victor.y, 0), mm_o), convert_point((Victor.x + u * cos(Victor.an_xy), Victor.y + u * sin(Victor.an_xy), 0), mm_o)], 2)
    circle(screen, BLACK, Vector(100, 111, 2000000).get_vector(Victor).coords_to_cam(Victor), 10)
    cub.draw_cube(screen, Victor)
    pygame.display.update()

pygame.display.update()