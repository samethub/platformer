import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, image_path):
        super().__init__()
        self.images = [pygame.image.load(image_path).convert_alpha(),
                       pygame.image.load("../graphics/character/player_1_hit.png").convert_alpha()]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.collide_rect = self.rect
        t, l, w, h = pos[0] - 16, pos[1] - 16, 48, 48
        self.damage_rect = pygame.Rect(t, l, w, h)

        # movement
        self.speed, self.jump_speed = 10, 16
        self.jump_pressed, self.can_jump = False, True
        self.jump_counter, self.jump_limit = 0, 1
        self.jump_time, self.jump_time_limit = 0, 300
        self.gravity = 0.75
        self.direction = pygame.math.Vector2()
        self.moving_right, self.moving_left = False, False

        # health
        self.health, self.max_health = 100, 100
        self.animate_hit = False
        self.hit_frame_index = 0
        self.frames_waited, self.frames_wait = 0, 5
        self.total_frames_waited, self.total_frames_wait = 0, 60

        # shooting
        self.bullet_left = 10
        self.total_bullets = 10
        self.current_bullet_level = 1
        self.reload_started = 0
        self.reload_time = 2000
        self.reloading = False
        self.bullets = {"1": pygame.image.load("../graphics/bullets/bullet_1.png").convert_alpha(),
                        "2": None,
                        "3": None}

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
        self.health -= 15

    def get_healing(self):
        self.health += 20
        if self.health > self.max_health:
            self.health = self.max_health

    def increment_health(self, amount=20):
        self.max_health += amount

    """input"""
    def get_input(self):
        keys = pygame.key.get_pressed()

        # horizontal movement check
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.moving_right = True
        else:
            self.moving_right = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.moving_left = True
        else:
            self.moving_left = False

        # vertical movement check
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.jump_pressed = True
        else:
            self.jump_pressed = False

        # bullet reload check
        if keys[pygame.K_r] and self.bullet_left != 10 and not self.reloading:
            self.reloading = True
            self.reload_gun()

        # bullet switch check
        if keys[pygame.K_1]:
            self.switch_bullets("1")
        elif keys[pygame.K_2]:
            self.switch_bullets("2")
        elif keys[pygame.K_3]:
            self.switch_bullets("3")

    """shooting"""
    def reload_gun(self):
        self.reload_started = pygame.time.get_ticks()

    def check_reload(self):
        if self.reloading:
            current_time = pygame.time.get_ticks()
            if (current_time - self.reload_started) >= self.reload_time:
                self.bullet_left = self.total_bullets
                self.reloading = False

    def get_horizontal_direction(self):
        if self.moving_left and self.moving_right:
            self.direction.x = 0
        elif self.moving_left:
            self.direction.x = -1
        elif self.moving_right:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def increment_bullet(self, amount=5):
        self.total_bullets += amount

    def add_bullet_2(self):
        if not self.bullets["2"]:
            self.bullets["2"] = pygame.image.load("../graphics/bullets/bullet_2.png").convert_alpha()
        else:
            self.total_bullets += 1

    def add_bullet_3(self):
        if not self.bullets["3"]:
            self.bullets["3"] = pygame.image.load("../graphics/bullets/bullet_3.png").convert_alpha()
        else:
            self.total_bullets += 1

    def switch_bullets(self, level="1"):
        if self.bullets[level]:
            self.current_bullet_level = int(level)
    """movement"""
    def horizontal_movement(self):
        self.get_horizontal_direction()
        self.collide_rect.x += self.speed * self.direction.x

    def vertical_movement(self):
        self.jump()
        self.apply_gravity()
        self.collide_rect.y += self.direction.y

    def check_can_jump(self):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.jump_time
        if delta_time >= self.jump_time_limit:
            self.can_jump = True

    def jump(self):
        self.check_can_jump()
        if self.jump_pressed and self.jump_counter <= self.jump_limit and self.can_jump:
            self.jump_counter += 1
            self.direction.y = - self.jump_speed
            self.can_jump = False
            self.jump_time = pygame.time.get_ticks()

    def add_jump(self):
        self.jump_limit += 1

    def apply_gravity(self):
        self.direction.y += self.gravity

    """rect pos"""
    def adjust_rect_pos(self):
        self.rect.topleft = self.collide_rect.topleft
        self.damage_rect.center = self.collide_rect.center

    """shift"""
    def shift_player(self, shift):
        self.collide_rect.x += shift[0]
        self.collide_rect.y += shift[1]

    def update(self, shift):
        self.shift_player(shift)
        self.get_input()
        self.animate()
        self.check_reload()

