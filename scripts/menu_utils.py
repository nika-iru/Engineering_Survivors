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