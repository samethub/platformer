import random

import pygame




class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image_surf):
        super().__init__()
        self.image = image_surf
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(pos[0], pos[1])

    def change_pos(self, shift):
        self.pos += shift

    def change_rect_pos(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def update(self, shift):
        self.change_pos(shift)
        self.change_rect_pos()


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos, image=None):
        super().__init__()
        if not image:
            self.image = pygame.Surface((64,64))
            self.image.fill("black")
            self.image.set_colorkey("black")
        else:
            self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(pos[0], pos[1])

    def change_pos(self, shift):
        self.pos += shift

    def change_rect_pos(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def update(self, shift):
        self.change_pos(shift)
        self.change_rect_pos()


class Gift(Tile):
    def __init__(self, pos, image_surf=None, mission=None):
        super(Gift, self).__init__(pos, image_surf)
        self.start_pos = pygame.math.Vector2(pos[0], pos[1])
        self.mission = mission
        self.apply_gravity = True
        self.jump_speed = -16
        self.gravity = 1
        self.direction = pygame.math.Vector2(0, self.jump_speed)

    def animate(self):
        if self.apply_gravity:
            self.direction.y += self.gravity
            self.pos += self.direction
            if self.pos.y + self.rect.height >= self.start_pos[1] and self.direction.y > 0:
                self.pos.y = self.start_pos[1] - self.rect.height
                self.apply_gravity = False

    def change_pos(self, shift):
        self.pos += shift
        self.start_pos += shift

    def update(self, shift):
        self.change_pos(shift)
        self.animate()
        self.change_rect_pos()


class Case(Icon):
    def __init__(self, pos, gift_group, player, image=None):
        super(Case, self).__init__(pos, image)
        self.gifts = [
            {"surf": pygame.image.load("../graphics/bullets/5bullet.png").convert_alpha(),
             "mission": player.increment_bullet,
             "increment": 5},
            {"surf": pygame.image.load("../graphics/environment/extra_health.png").convert_alpha(),
             "mission": player.increment_health,
             "increment": 20},
            {"surf": pygame.transform.scale(pygame.image.load("../graphics/bullets/bullet_2.png").convert_alpha(),
                                            (64, 64)),
             "mission": player.add_bullet_2,
             "increment": None},
            {"surf": pygame.transform.scale(pygame.image.load("../graphics/bullets/bullet_3.png").convert_alpha(),
                                            (64, 64)),
             "mission": player.add_bullet_3,
             "increment": None},
            {"surf": pygame.image.load("../graphics/environment/extra_jump.png").convert_alpha(),
             "mission": player.add_jump,
             "increment": None
            }
        ]
        self.status = "locked"
        self.gift_group = gift_group

    def give_gift(self):
        gift = random.choice(self.gifts)
        self.gift_group.add(Gift(self.rect.topleft, gift["surf"], gift["mission"]))
