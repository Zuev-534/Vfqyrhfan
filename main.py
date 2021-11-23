from vocabulary import *
from Camera import *

Victor = Camera()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Test controlling')
# pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
while True:
    clock.tick(FPS)
    screen.fill(GREY1)
    for event in pygame.event.get():
        Victor.interoperate(event)
        Victor.control()
    Victor.move()
    coords(screen, Victor)
    circle(screen, BLACK, (Victor.x, Victor.y,), 5)
    circle(screen, BLACK, (100,100), 5)

    circle(screen, BLACK, Vector(100, 100, 0).get_vector(Victor).coords_to_cam(), 10)
    pygame.display.update()