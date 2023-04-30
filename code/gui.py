import pygame


class HealthBar:
    def __init__(self, pos, health, max_health, func):
        self.player_dead = func
        self.health = health
        self.max_health = max_health
        self.image = pygame.image.load("../graphics/gui/health_bar.png").convert_alpha()
        self.image_rect = self.image.get_rect(topleft=pos)
        self.get_width()

        self.bar_surf = pygame.Surface((self.width, 64))
        self.bar_surf.fill("#950101")
        self.bar_x, self.bar_y = self.image_rect.topleft[0] + 64, self.image_rect.topleft[1]
        self.bar_rect = self.bar_surf.get_rect(topleft=(self.bar_x, self.bar_y))

    def get_width(self):
        # self.width = int(256 - 256*(100 - health)/100)
        self.width = int(self.health / self.max_health * (self.image_rect.width / 5 * 4))

    def new_bar_object(self):
        self.bar_surf = pygame.Surface((self.width, 64))
        self.bar_surf.fill("#950101")
        self.bar_x, self.bar_y = self.image_rect.topleft[0] + 64, self.image_rect.topleft[1]
        self.bar_rect = self.bar_surf.get_rect(topleft=(self.bar_x, self.bar_y))

    def update(self, new_health, max_health):
        if new_health >= 0:
            self.max_health = max_health
            self.health = new_health
            self.get_width()
            self.new_bar_object()
        elif new_health < 0:
            self.width = 0
            self.new_bar_object()
            self.player_dead()
            print("dead")
            # player dead

    def draw(self, surface):
        surface.blit(self.bar_surf, self.bar_rect)
        surface.blit(self.image, self.image_rect)


class BulletCap:
    def __init__(self, pos, total_bullets, current_bullets, bullet_level):
        self.total_bullets = total_bullets
        self.bullet_level = bullet_level
        self.current_bullets = current_bullets
        self.pos = (pos[0] + 64, pos[1])
        self.font = pygame.font.Font("../graphics/gui/ARCADEPI.TTF", 32)

        self.bullet_surfaces = {
            "1": pygame.image.load("../graphics/bullets/bullet_1.png").convert_alpha(),
            "2": pygame.image.load("../graphics/bullets/bullet_2.png").convert_alpha(),
            "3": pygame.image.load("../graphics/bullets/bullet_3.png").convert_alpha(),
        }
        self.bullet_surf = pygame.transform.scale(self.bullet_surfaces[f"{self.bullet_level}"],
                                                  (32, 32))
        self.bullet_rect = self.bullet_surf.get_rect(topleft=pos)

        self.text = f"{current_bullets} / {total_bullets}"
        self.surf = self.font.render(self.text, False, "black")
        self.rect = self.surf.get_rect(topleft=self.pos)

    def update(self, current_bullets, total_bullets, bullet_level):
        self.bullet_level = bullet_level
        self.total_bullets = total_bullets
        self.current_bullets = current_bullets

        self.bullet_surf = pygame.transform.scale(self.bullet_surfaces[f"{self.bullet_level}"],
                                                  (32, 32))
        self.bullet_rect = self.bullet_surf.get_rect(topleft=self.bullet_rect.topleft)

        self.text = f"{self.current_bullets} / {self.total_bullets}"
        self.surf = self.font.render(self.text, False, "black")
        self.rect = self.surf.get_rect(topleft=self.pos)

    def draw(self, surface):
        surface.blit(self.bullet_surf, self.bullet_rect)
        surface.blit(self.surf, self.rect)


class EnemyCap:
    def __init__(self, pos, total_enemies, current_enemies, level=0):
        self.total_enemies = total_enemies
        self.current_enemies = current_enemies
        self.pos = (pos[0] + 64, pos[1])
        self.font = pygame.font.Font("../graphics/gui/ARCADEPI.TTF", 32)
        self.enemy_level = level
        self.enemy_icon = pygame.image.load("../graphics/enemy/enemy_1.png").convert_alpha()
        self.enemy_icon = pygame.transform.rotozoom(self.enemy_icon, 0, 1/2)
        self.enemy_rect = self.enemy_icon.get_rect(topleft=pos)

        self.text = f"{current_enemies} / {total_enemies}"
        self.surf = self.font.render(self.text, False, "black")
        self.rect = self.surf.get_rect(topleft=self.pos)

    def update(self, current_enemies, level):
        self.current_enemies = current_enemies

        self.text = f"{self.current_enemies} / {self.total_enemies}"
        self.surf = self.font.render(self.text, False, "black")
        self.rect = self.surf.get_rect(topleft=self.pos)

        if self.enemy_level != level:
            self.enemy_icon = pygame.image.load("../graphics/enemy/enemy_1.png").convert_alpha()
            self.enemy_icon = pygame.transform.rotozoom(self.enemy_icon, 0, 1 / 2)
            self.enemy_rect = self.enemy_icon.get_rect(topleft=self.enemy_rect.topleft)

    def draw(self, surface):
        surface.blit(self.enemy_icon, self.enemy_rect)
        surface.blit(self.surf, self.rect)


class Statistics:
    def __init__(self, surface, kill, damage_got, time, win):
        self.display_surface = surface
        self.win = win
        kill_text, damage_text, time_text = f"Kill: {kill}", f"Damage: {damage_got}", f"Time: {time}"
        if win:
            self.font = pygame.font.Font("../graphics/gui/ARCADEPI.TTF", 128)
            self.win_surf = self.font.render("You Won", True, "green")
            self.win_rect = self.win_surf.get_rect(center=(self.display_surface.get_width() // 2, 200))

            self.kill_surface = self.font.render(kill_text, False, "red")
            self.damage_surface = self.font.render(damage_text, False, "red")
            self.time_surface = self.font.render(time_text, False, "red")

            self.kill_rect = self.kill_surface.get_rect(topleft=(100, 400))
            self.damage_rect = self.damage_surface.get_rect(topleft=(100, 500))
            self.time_rect = self.time_surface.get_rect(topleft=(100, 600))
        else:
            self.font = pygame.font.Font("../graphics/gui/ARCADEPI.TTF", 72)
            self.kill_surface = self.font.render(kill_text, False, "red")
            self.damage_surface = self.font.render(damage_text, False, "red")
            self.time_surface = self.font.render(time_text, False, "red")

            self.kill_rect = self.kill_surface.get_rect(topleft=(100, 200))
            self.damage_rect = self.damage_surface.get_rect(topleft=(100, 350))
            self.time_rect = self.time_surface.get_rect(topleft=(100, 500))

    def draw(self):
        self.display_surface.blit(self.kill_surface, self.kill_rect)
        self.display_surface.blit(self.damage_surface, self.damage_rect)
        self.display_surface.blit(self.time_surface, self.time_rect)
        if self.win:
            self.display_surface.blit(self.win_surf, self.win_rect)

















