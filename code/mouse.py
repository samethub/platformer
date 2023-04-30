import pygame


class Cursor:
    def __init__(self, pos):
        self.image = pygame.image.load("../graphics/curser/curser.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

