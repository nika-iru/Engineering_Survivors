import pygame
import math
import sys

class Button:

    def __init__(self, menu, size, pos):
        self.menu = menu
        self.size = size
        self.pos = list(pos)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def render(self, surf, key, index):
        surf.blit(self.menu.assets[key][index], (self.pos[0], self.pos[1]))

    def select(self, surf):
        surf.blit(self.menu.assets['select'], (self.pos[0], self.pos[1]))

class Cloud:
    def __init__(self, game, size, pos, asset, index, speed):
        self.game = game
        self.size = size
        self.pos = list(pos)
        self.asset = asset
        self.index = index
        self.speed = 0

    def center(self):
        return pygame.Vector2(self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2)

    def render(self, surf, index, asset):
        # Use the camera to adjust the background's position
        cloud_pos = self.pos
        surf.blit(pygame.transform.scale(self.game.assets[asset][index], ((self.game.assets[asset][index].get_width() * 3), (self.game.assets[asset][index].get_height() * 3))), cloud_pos)

    def rect(self):  # this refers to the upper right pixel of the entity
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self):
        self.pos[0] -= self.speed