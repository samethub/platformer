import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.image.load("../graphics/bullets/bullet_1.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos

        # movement
        self.speed = 12
        self.direction = pygame.math.Vector2(int(direction[0] * self.speed), int(direction[1] * self.speed))

    def move(self):
        self.pos += (self.direction.x, self.direction.y)

    def shift_bullet(self, shift):
        self.pos += shift

    def change_rect_pos(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def update(self, shift):
        self.shift_bullet(shift)
        self.move()
        self.change_rect_pos()


class BulletOne(Bullet):
    def __init__(self, pos, direction):
        super().__init__(pos, direction)
        self.image = pygame.image.load("../graphics/bullets/bullet_1.png").convert_alpha()


class BulletTwo(Bullet):
    def __init__(self, pos, direction):
        super().__init__(pos, direction)
        self.image = pygame.image.load("../graphics/bullets/bullet_2.png").convert_alpha()
        self.speed = 13


class BulletThree(Bullet):
    def __init__(self, pos, direction):
        super().__init__(pos, direction)
        self.image = pygame.image.load("../graphics/bullets/bullet_3.png").convert_alpha()
        self.speed = 15


class EnemyBulletOne(Bullet):
    def __init__(self, pos, create_explosion_effect):
        super().__init__(pos, direction=(0, 0))
        self.image = pygame.image.load("../graphics/bullets/enemy_bullet_1.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.speed = 6

        # live
        self.created = pygame.time.get_ticks()
        self.stay_alive = 3000

        # imports
        self.create_explosion_effect = create_explosion_effect

    """explosion"""
    def check_explosion(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.created >= self.stay_alive:
            self.kill()
            self.create_explosion_effect(self.rect.center)

    """movement"""
    def move(self):
        x = int(self.direction.x * self.speed)
        y = int(self.direction.y * self.speed)
        self.pos += (x, y)

    def change_direction(self, player_pos):
        player_pos = pygame.math.Vector2(player_pos[0], player_pos[1])
        self_pos = pygame.math.Vector2(self.pos[0], self.pos[1])

        try:
            self.direction = (player_pos - self_pos).normalize()
        except ValueError:
            print("got shot")
            self.kill()

    def update(self, shift, player_pos):
        self.check_explosion()
        self.change_direction(player_pos)
        self.shift_bullet(shift)
        self.move()
        self.change_rect_pos()


class EnemyBulletTwo(EnemyBulletOne):
    def __init__(self, pos, create_explosion_effect):
        super().__init__(pos, create_explosion_effect)
        self.image = pygame.image.load("../graphics/bullets/enemy_bullet_2.png").convert_alpha()
        self.stay_alive = 4000
        self.speed = 8

