import random

import pygame
from game_data import level_0
from support import import_cut_graphics, import_data
from tile import Tile, Icon, Case
from settings import *
from player import Player
from enemy import Enemy, EnemyTwo
from mouse import Cursor
from bullets import EnemyBulletOne, BulletOne, EnemyBulletTwo, BulletTwo, BulletThree
from effects import ExplosionEffect
from gui import HealthBar, BulletCap, EnemyCap, Statistics
from random import choice

class Level:
    def __init__(self, surface):
        # basic setup
        self.display_surface = surface

        # game over surf
        self.game_over_surf = pygame.Surface(self.display_surface.get_size())
        self.game_over_surf.fill("white")
        self.game_over_surf.set_alpha(180)
        self.game_over_rect = self.game_over_surf.get_rect(topleft=(0, 0))
        self.statistics = None
        self.damage = 0
        self.game_start_time = pygame.time.get_ticks()

        # mouse
        self.cursor = Cursor(pygame.mouse.get_pos())
        pygame.mouse.set_visible(False)
        self.mouse_down = False

        # player setup
        player_data = import_data(level_0["player"])
        img_path = "../graphics/character/player_1.png"
        self.player = self.setup_player(player_data, img_path)
        self.player_dead = False
        self.win = False

        # bullets
        self.bullet_group = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        # camera direction
        self.world_shift = pygame.math.Vector2()
        self.camera_direction = pygame.math.Vector2()

        # stars
        self.stars_data = import_data(level_0["stars"])
        img_path = "../graphics/environment/two_stars.png"
        self.stars_tile_lst = import_cut_graphics(img_path)
        self.stars_group = self.setup_tiles("stars", self.stars_data)

        # terrain setup
        self.terrain_data = import_data(level_0["terrain"])
        img_path = "../graphics/terrain/terrain_1.png"
        self.terrain_tile_list = import_cut_graphics(img_path)
        self.terrain_group = self.setup_tiles("terrain", self.terrain_data)

        # enemy setup
        self.enemy_data = import_data(level_0["enemies"]["data"])
        self.enemy_images = level_0["enemies"]["images"]
        self.enemy_group = self.setup_tiles("enemy", self.enemy_data)
        self.enemy_icon = self.setup_tiles("enemy_icon", self.enemy_data)
        self.enemy_level = 0

        # decoration
        self.e_bullet_explosions = pygame.sprite.Group()
        self.health_bar = HealthBar((40, 50), self.player.sprite.health, self.player.sprite.max_health, self.change_player_dead)
        self.bullet_cap = BulletCap((40, 120), self.player.sprite.total_bullets,
                                    self.player.sprite.bullet_left, 1)
        self.enemy_cap = EnemyCap((40, 190), len(self.enemy_group), len(self.enemy_group), self.enemy_level)
        self.gift = pygame.sprite.Group()
        self.case_group = self.setup_tiles("case", import_data(level_0["case"]))
        self.can_unlock = True
        sprite = random.choice(self.case_group.sprites())
        sprite.status = "unlocked"
        sprite.image = pygame.image.load("../graphics/environment/case_unlocked.png").convert_alpha()

        self.heart_icons = self.setup_tiles("heart", import_data(level_0["heart"]))
        self.heart_group = pygame.sprite.Group()
        self.collidable_sprites = self.terrain_group.sprites() + self.case_group.sprites()

    """setup sprite groups"""
    def setup_player(self, data, img_path):
        group = pygame.sprite.GroupSingle()
        for row_ind, row in enumerate(data):
            for col_ind, val in enumerate(row):

                if val != "-1":
                    x = (col_ind * TILE_SIZE)
                    y = (row_ind * TILE_SIZE)
                    pos = (x, y)
                    group.add(Player(pos, img_path))
                    break
        return group

    def setup_tiles(self, type, data, level=0):
        group = pygame.sprite.Group()

        for row_ind, row in enumerate(data):
            for col_ind, val in enumerate(row):

                if val != "-1":
                    x = (col_ind * TILE_SIZE)
                    y = (row_ind * TILE_SIZE)
                    pos = (x, y)

                    if type == "terrain":
                        group.add(Tile(pos, self.terrain_tile_list[int(val)]))
                    if type == "enemy":
                        group.add(Enemy(pos, self.enemy_images[level], self.change_can_unlock))
                    if type == "enemy_icon":
                        group.add(Icon(pos))
                    if type == "case":
                        group.add(Case(pos, self.gift, self.player.sprite, "../graphics/environment/case_locked.png"))
                    if type == "heart":
                        group.add(Icon(pos))
                    if type == "stars":
                        group.add(Tile(pos, self.stars_tile_lst[int(val)]))
        return group

    """camera"""
    def check_camera_distance(self):
        self.camera_direction.x = (SCREEN_W // 2) - self.player.sprite.rect.centerx
        self.camera_direction.y = (SCREEN_H // 2) - self.player.sprite.rect.centery

        self.world_shift = self.camera_direction // 25

    """collisions"""
    def check_horizontal_collisions(self):
        player = self.player.sprite
        player.horizontal_movement()
        collidable_sprites = self.collidable_sprites

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collide_rect):
                if player.direction.x < 0:  # moving left
                    player.collide_rect.left = sprite.rect.right

                elif player.direction.x > 0:  # moving right
                    player.collide_rect.right = sprite.rect.left

    def check_vertical_collisions(self):
        player = self.player.sprite
        player.vertical_movement()
        collidable_sprites = self.collidable_sprites

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collide_rect):
                if player.direction.y < 0:  # moving up
                    player.collide_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                elif player.direction.y > player.gravity:  # moving dowm
                    player.collide_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.jump_counter = 0

    def check_bullet_case_collision(self):
        case = [sprite for sprite in self.case_group.sprites() if sprite.status == "unlocked"]
        print(len(case))
        if case:
            case = case[0]
            if pygame.sprite.spritecollide(case, self.bullet_group, dokill=True):
                case.status = "locked"
                case.image = pygame.image.load("../graphics/environment/case_locked.png").convert_alpha()
                case.give_gift()
                self.can_unlock = False

    def check_player_gift_collision(self):
        if self.gift:
            for gift in self.gift.sprites():
                if pygame.sprite.spritecollide(gift, self.player, False):
                    gift.mission()
                    gift.kill()

    def check_player_got_shot(self):
        for bullet in self.enemy_bullets.sprites():
            if self.player.sprite.damage_rect.colliderect(bullet.rect):
                bullet.kill()
                self.player.sprite.get_damage()
                self.damage += -15

    def check_bullet_hit_bullet(self):
        collide_dict = pygame.sprite.groupcollide(self.bullet_group, self.enemy_bullets, True, False)
        if collide_dict:
            for _, bullet in collide_dict.items():
                bullet = bullet[0]
                effect = ExplosionEffect(bullet.rect.center, "orange")
                self.e_bullet_explosions.add(effect)
                bullet.kill()

    def check_enemy_got_shot(self):
        collide_dict = pygame.sprite.groupcollide(self.bullet_group, self.enemy_group, False, False)
        # key is bullet, value is enemy
        if collide_dict:
            for bullet, enemy in collide_dict.items():
                enemy = enemy[0]
                if enemy.damage_rect.colliderect(bullet.rect):
                    bullet.kill()
                    enemy.get_damage()
                    if not self.enemy_group:
                        self.create_new_enemies()

    def check_player_heart_collision(self):
        if pygame.sprite.groupcollide(self.player, self.heart_group, False, True):
            self.player.sprite.get_healing()

    """mouse"""
    def check_mouse_clicks(self):
        if pygame.mouse.get_pressed()[0] and not self.mouse_down:
            player = self.player.sprite
            if player.bullet_left != 0 and not player.reloading:
                self.mouse_down = True
                player.bullet_left -= 1
                direction = self.get_bullet_direction()
                self.create_bullet(direction)
        elif not pygame.mouse.get_pressed()[0]:
            self.mouse_down = False

    """bullet"""
    def get_bullet_direction(self):
        player_pos = pygame.math.Vector2(self.player.sprite.rect.centerx, self.player.sprite.rect.centery)
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        direction = (mouse_pos - player_pos).normalize()
        return direction

    def create_bullet(self, direction):
        level = self.player.sprite.current_bullet_level
        if level == 1:
            bullet = BulletOne(self.player.sprite.rect.center, direction)
        elif level == 2:
            bullet = BulletTwo(self.player.sprite.rect.center, direction)
        elif level == 3:
            bullet = BulletThree(self.player.sprite.rect.center, direction)
        self.bullet_group.add(bullet)

    def check_bullet_kill(self):
        for bullet in self.bullet_group.sprites():
            if bullet.rect.x < -SCREEN_W or bullet.rect.x > 2*SCREEN_W:
                bullet.kill()
            elif bullet.rect.y < -SCREEN_H or bullet.rect.y > 2*SCREEN_H:
                bullet.kill()

    """enemy"""
    def create_new_enemies(self):
        for sprite in self.enemy_icon.sprites():
            pos = sprite.rect.topleft
            enemy = EnemyTwo(pos, self.enemy_images[1], self.change_can_unlock)
            self.enemy_group.add(enemy)
        self.enemy_level += 1
        if self.enemy_level == 2:
            self.win = True

    def check_player_in_enemy_zone(self):
        p_pos = self.player.sprite.rect.center
        for sprite in self.enemy_group.sprites():
            # rect = sprite.range_rect
            s_pos = sprite.rect.center
            delta = ((p_pos[0]-s_pos[0])**2 + (p_pos[1]-s_pos[1])**2) ** (1/2)
            if delta <= sprite.range / 3*2 and sprite.can_shoot:
                sprite.can_shoot = False
                sprite.start_shoot_timer()
                if self.enemy_level == 0:
                    bullet = EnemyBulletOne(sprite.rect.center, self.create_explosion_effect)
                elif self.enemy_level == 1:
                    bullet = EnemyBulletTwo(sprite.rect.center, self.create_explosion_effect)
                else:
                    bullet = EnemyBulletOne(sprite.rect.center, self.create_explosion_effect)

                self.enemy_bullets.add(bullet)

    """explosion"""
    def create_explosion_effect(self, pos):
        effect = ExplosionEffect(pos, "blue")
        self.e_bullet_explosions.add(effect)

    """environment"""
    def create_heart(self):
        if len(self.heart_group) < 1:
            pos = choice(self.heart_icons.sprites()).rect.topleft
            self.heart_group.add(Icon(pos, "../graphics/environment/heart.png"))

    def check_unlocked_case(self):
        unlocked_cases = [sprite for sprite in self.case_group.sprites() if sprite.status == "unlocked"]
        if len(self.enemy_group) % 1 == 0 and not unlocked_cases and self.can_unlock:
            sprite = random.choice(self.case_group.sprites())
            sprite.status = "unlocked"
            sprite.image = pygame.image.load("../graphics/environment/case_unlocked.png").convert_alpha()

    def change_can_unlock(self):
        if not self.can_unlock:
            self.can_unlock = not self.can_unlock

    """player dead"""
    def change_player_dead(self):
        self.player_dead = True


    def run(self):

        if not self.player_dead or not self.win:
            """updates"""
            # stars
            self.stars_group.update(self.world_shift)
            # terrain
            self.terrain_group.update(self.world_shift)
            # enemy
            self.enemy_group.update(self.world_shift)
            self.enemy_icon.update(self.world_shift)
            # player
            self.player.update(self.world_shift)
            # mouse
            self.cursor.update()
            # bullets
            self.bullet_group.update(self.world_shift)
            self.enemy_bullets.update(self.world_shift, self.player.sprite.rect.center)
            # decoration
            self.e_bullet_explosions.update(self.world_shift)
            self.health_bar.update(self.player.sprite.health, self.player.sprite.max_health)
            self.bullet_cap.update(self.player.sprite.bullet_left, self.player.sprite.total_bullets,
                                   self.player.sprite.current_bullet_level)
            self.enemy_cap.update(len(self.enemy_group), self.enemy_level)
            self.case_group.update(self.world_shift)
            self.heart_icons.update(self.world_shift)
            self.heart_group.update(self.world_shift)
            self.gift.update(self.world_shift)

            """collision checks"""
            self.check_horizontal_collisions()
            self.check_vertical_collisions()

            self.player.sprite.adjust_rect_pos()

            """checks"""
            self.check_camera_distance()
            self.check_mouse_clicks()

            self.check_bullet_case_collision()
            self.check_player_gift_collision()
            self.check_bullet_kill()
            self.check_bullet_hit_bullet()
            self.check_player_in_enemy_zone()
            self.check_player_got_shot()
            self.check_enemy_got_shot()
            self.check_player_heart_collision()
            self.create_heart()
            self.check_unlocked_case()

        """draw"""
        # stars
        self.stars_group.draw(self.display_surface)
        # terrain
        self.terrain_group.draw(self.display_surface)
        # bullets
        self.bullet_group.draw(self.display_surface)
        self.enemy_bullets.draw(self.display_surface)
        # enemy
        self.enemy_group.draw(self.display_surface)
        # player
        self.player.draw(self.display_surface)
        # decoration
        self.e_bullet_explosions.draw(self.display_surface)
        self.case_group.draw(self.display_surface)
        self.bullet_cap.draw(self.display_surface)
        self.enemy_cap.draw(self.display_surface)
        self.heart_icons.draw(self.display_surface)
        self.heart_group.draw(self.display_surface)
        self.health_bar.draw(self.display_surface)
        self.gift.draw(self.display_surface)
        # mouse
        self.display_surface.blit(self.cursor.image, self.cursor.rect)

        if self.player_dead or self.win:
            """create stats"""
            if not self.statistics:
                current_time = pygame.time.get_ticks()
                delta = (current_time - self.game_start_time) // 1000
                kill = self.enemy_level * 14 + 14 - len(self.enemy_group)
                self.statistics = Statistics(self.display_surface, kill, self.damage, delta, self.win)

            """draw"""
            self.display_surface.blit(self.game_over_surf, self.game_over_rect)
            self.statistics.draw()
            """check input"""
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player_dead = False
                self.__init__(self.display_surface)




