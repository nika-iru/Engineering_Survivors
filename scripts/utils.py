import os
import pygame

BASE_IMG_PATH = 'data/img/'

BASE_MUSIC_PATH = 'data/music/'

BASE_SFX_PATH = 'data/music/'

pygame.mixer.init()
pygame.init()

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey((255,255,255))
    return img

def load_images(path): # used to load everything in one folder
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)): # takes every img in the directory appending it on a list / sorted alphabetically use 01 instead of 1
        images.append(load_image(path + '/' + img_name))
    return images

def load_music(path):
    music = BASE_MUSIC_PATH + path
    return music

def load_sfx(path):
    sfx_path = BASE_SFX_PATH + path
    sfx = pygame.mixer.Sound(sfx_path)
    return sfx

class Timer:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()

    def get_elapsed_time(self):
        return pygame.time.get_ticks() - self.start_time

    def reset_timer(self):
        self.start_time = pygame.time.get_ticks()