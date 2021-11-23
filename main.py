from vocabulary import *
from Camera import *

points = (Vector(100, 100, 0), Vector(50, 50, 0), Vector(10, 20, 0), Vector(-10, 20, 0), Vector(10, 10, 10))
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
    pygame.display.update()
    for point in points:
        pygame.circle(screen, 'green', point.get_vector(Victor), 10)
