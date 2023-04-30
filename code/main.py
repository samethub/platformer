import pygame, sys
from settings import SCREEN_W, SCREEN_H
from level import Level


pygame.init()

# screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
screen = pygame.display.set_mode((0, 0), flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()

level = Level(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # screen.fill("#917FB3")aaaw
    screen.fill("#AFD3E2")
    level.run()
    pygame.display.update()
    clock.tick(60)