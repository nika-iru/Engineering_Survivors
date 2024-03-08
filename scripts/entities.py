import pygame
import math
import sys


class Player:
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size

        # player stats
        self.base_hp = 4
        self.health = self.base_hp

        self.base_damage = 3
        self.damage = self.base_damage

        self.base_mvspd = 2
        self.mvspd = self.base_mvspd

        self.base_atkspd = 50
        self.atkspd = self.base_atkspd

        self.invul = False
        self.invul_timer = 0

        self.currentXP = 14
        self.neededXP = 15
        self.playerlvl = 1

    def rect(self):  # this refers to the upper right pixel of the entity
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, movement = (0, 0)):
        dx, dy = movement

        # Normalize the movement vector
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length != 0:
            dx /= length
            dy /= length

        # Update player position
        self.pos[0] += dx * self.mvspd
        self.pos[1] += dy * self.mvspd

        if self.health <= 0:
            pygame.quit()
            sys.exit()

    def center(self):
        return pygame.Vector2(self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2)

    def render(self, surf, camera, mouse_x):
        # Use the camera to adjust the player's position
        player_pos_on_screen = camera.apply(self.pos)
        player_flipped = pygame.transform.flip(self.game.assets['player'][0], True, False).convert_alpha()
        player_flipped.set_colorkey((255,255,255))
        if mouse_x > self.pos[0]:
            surf.blit(player_flipped, player_pos_on_screen)
        if mouse_x < self.pos[0]:
            surf.blit(self.game.assets['player'][0], player_pos_on_screen)

    def take_dmg(self, damage):
        mvspd_buff = self.mvspd/2
        self.base_spd = self.mvspd
        if not self.invul:
            self.health -= damage
            self.mvspd += mvspd_buff

    def apply_invulnerability(self):
        self.invul = True
        self.invul_timer = pygame.time.get_ticks()


class Camera:
    def __init__(self, game, target):
        self.game = game
        self.target = target

    def apply(self, entity):
        return entity - self.target + pygame.Vector2(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2)

    def apply_inverse(self, screen_pos):
        return screen_pos + self.target - pygame.Vector2(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2)


class Enemy:
    def __init__(self, game, pos, size, eHP, eSpd, xpWorth):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.eHP = eHP
        self.eSpd = eSpd
        self.eXP = xpWorth

    def rect(self):  # this refers to the upper right pixel of the entity
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, player):
        angle_to_player = math.atan2(player.pos[1] - self.pos[1], player.pos[0] - self.pos[0])
        self.pos[0] += self.eSpd * math.cos(angle_to_player)
        self.pos[1] += self.eSpd * math.sin(angle_to_player)

    def render(self, surf, camera):
        # Use the camera to adjust the player's position
        enemy_pos_on_screen = camera.apply(self.pos)
        surf.blit(self.game.assets['student'][0], enemy_pos_on_screen)


class Bullet:
    def __init__(self, game, pos, size, speed, interval, remove, direction):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.speed = speed
        self.interval = interval
        self.remove = remove
        self.direction = pygame.Vector2(direction[0] - self.pos[0], direction[1] - self.pos[1]).normalize()

    def update(self):
        # Update bullet position
        self.pos[0] += self.direction.x * self.speed
        self.pos[1] += self.direction.y * self.speed

    def rect(self):  # this refers to the upper right pixel of the entity
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def render(self, surf, camera):
        bullet_initial_pos = camera.apply(self.pos)
        surf.blit(self.game.assets['bullet'][0], bullet_initial_pos)


class Background:
    def __init__(self, game, size, pos):
        self.game = game
        self.size = size
        self.pos = list(pos)

    def center(self):
        return pygame.Vector2(self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2)

    def render(self, surf, camera, asset, index):
        # Use the camera to adjust the background's position
        bg_pos = camera.apply(self.pos)
        surf.blit(self.game.assets[asset][index], bg_pos)


class Chunk:
    def __init__(self, game, pos):
        self.game = game
        self.pos = list(pos)


class Sprite:
    def __init__(self, game, size, pos, asset):
        self.game = game
        self.size = size
        self.pos = list(pos)
        self.asset = asset

    def center(self):
        return pygame.Vector2(self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2)

    def render(self, surf, camera, index):
        # Use the camera to adjust the background's position
        card_pos = camera.apply(self.pos)
        surf.blit(self.game.assets[self.asset][index], card_pos)

    def rect(self):  # this refers to the upper right pixel of the entity
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])




