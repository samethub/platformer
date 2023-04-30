import pygame
from random import choice
from pygame.math import Vector2 as vector


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, images, change_unlock):
        super().__init__()
        self.change_unlock = change_unlock
        self.images = [pygame.image.load(images[0]).convert_alpha(),
                       pygame.image.load(images[1]).convert_alpha()]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)

        self.pos = vector(pos[0], pos[1])
        t, l, w, h = 0,0, self.rect.width /4*3, self.rect.height /4*3
        self.damage_rect = pygame.Rect(t,l,w,h)
        self.damage_rect.center = self.rect.center

        # range rect
        self.range = 512
        self.range_surf = pygame.Surface((self.range, self.range))
        self.range_surf.fill("green")
        self.range_surf.set_colorkey("black")
        self.range_rect = self.range_surf.get_rect(center=self.rect.center)
        self.range_rect_pos = vector(self.range_rect.x, self.range_rect.y)

        # movement
        self.speed = 2
        choice_lst = [-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2]
        self.direction = vector(choice(choice_lst), choice(choice_lst))

        # shooting
        self.can_shoot = True
        self.shoot_time = 0
        self.shoot_wait = 1500

        # health
        self.animate_hit = False
        self.hit_frame_index = 0
        self.frames_waited, self.frames_wait = 0, 5
        self.total_frames_waited, self.total_frames_wait = 0, 60

        self.hit_limit = 5
        self.got_hit = 0

    """animation"""
    def animate(self):
        if self.animate_hit:
            if self.hit_frame_index == 1:
                self.image = self.images[self.hit_frame_index]
                self.frames_waited += 1
                if self.frames_waited >= self.frames_wait:
                    self.total_frames_waited += self.frames_waited
                    self.hit_frame_index = 0
                    self.frames_waited = 0
            elif self.hit_frame_index == 0:
                self.image = self.images[self.hit_frame_index]
                self.frames_waited += 1
                if self.frames_waited >= self.frames_wait:
                    self.total_frames_waited += self.frames_waited
                    self.frames_waited = 0
                    self.hit_frame_index = 1

            if self.total_frames_waited >= self.total_frames_wait:
                self.total_frames_waited = 0
                self.animate_hit = False
                self.image = self.images[0]

    """health"""
    def get_damage(self):
        self.animate_hit = True
        self.got_hit += 1
        if self.got_hit >= self.hit_limit:
            self.kill()
            self.change_unlock()

    """shooting"""
    def start_shoot_timer(self):
        self.shoot_time = pygame.time.get_ticks()

    def check_can_shoot(self):
        if self.shoot_time != 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_wait:
                self.can_shoot = True

    """movement"""
    def change_direction(self):
        if self.pos[0] <= self.range_rect.left:
            self.direction.x = abs(self.direction.x)
        if self.pos[0] >= self.range_rect.right:
            self.direction.x = abs(self.direction.x) * -1
        if self.pos[1] <= self.range_rect.top:
            self.direction.y = abs(self.direction.y)
        if self.pos[1] >= self.range_rect.bottom:
            self.direction.y = abs(self.direction.y) * -1

    def move(self):
        self.change_direction()
        x = int(self.direction.x * self.speed)
        y = int(self.direction.y * self.speed)
        self.pos += (x, y)

    def shift_enemy(self, shift):
        self.pos += shift
        self.range_rect_pos += shift

    def change_rect_pos(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        self.range_rect.x = self.range_rect_pos.x
        self.range_rect.y = self.range_rect_pos.y

        self.damage_rect.center = self.rect.center

    def update(self, shift):
        self.shift_enemy(shift)
        self.move()
        self.change_rect_pos()
        self.check_can_shoot()
        self.animate()


class EnemyTwo(Enemy):
    def __init__(self, pos, images, change_unlock):
        super(EnemyTwo, self).__init__(pos, images, change_unlock)
        self.speed = 3
        self.shoot_wait = 1000
        self.hit_limit = 7
        self.range = 512+128



