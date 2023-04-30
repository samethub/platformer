import pygame


class ExplosionEffect(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.radius = 5
        self.thickness = 30
        self.limit = 40
        self.speed = 3

        self.color = color
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill("white")
        self.image.set_colorkey("white")
        pygame.draw.circle(self.image, self.color, pos, self.radius, width=self.thickness)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos

    def scale_circle(self):
        self.radius += self.speed
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill("white")
        self.image.set_colorkey("white")
        pygame.draw.circle(self.image, self.color, self.image.get_rect().center, self.radius, width=self.thickness)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shift_effect(self, shift):
        self.pos += shift

    def change_rect_pos(self):
        self.rect.center = (self.pos[0], self.pos[1])
        # self.rect.x = self.pos.x
        # self.rect.y = self.pos.y

    def check_death(self):
        if self.radius >= self.limit:
            self.kill()

    def update(self, shift):
        self.check_death()
        self.shift_effect(shift)
        self.scale_circle()
        self.change_rect_pos()

