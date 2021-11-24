from vocabulary import *
from Camera import *

Victor = Camera()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Test controlling')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
u = 15
Victor.x, Victor.y = 0, 100
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
cub = Cube(0, 0, 0)
cubu = Cube(3, 3, 3)
cub.set_coords_with_move()
cubu.set_coords_with_move()
cub.print_all()
while True:
    clock.tick(FPS)
    screen.fill(GREY1)
    for event in pygame.event.get():
        Victor.interoperate(event)
        Victor.control()
    Victor.move()
    coords(screen, Victor)
    circle(screen, BLACK, convert_point((Victor.x, Victor.y, Victor.z), (mm_o)), 5)
    circle(screen, BLACK, convert_point((10, 100, 0), (mm_o)), 5)

    circle(screen, BLACK, Vector(10, 100, 0).get_vector(Victor).coords_to_cam(Victor), 10)
    pygame.draw.lines(screen, WHITE, True,
                      [convert_point((Victor.x, Victor.y, 0), (mm_o)),
                       convert_point((Victor.x + u * cos(Victor.an_xy), Victor.y + u * sin(Victor.an_xy), 0), (mm_o))], 2)
    pygame.display.update()