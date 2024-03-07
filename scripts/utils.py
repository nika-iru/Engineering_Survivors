import os

import pygame

BASE_IMG_PATH = 'data/img/'


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey((255,255,255))
    return img


def load_images(path): # used to load everything in one folder
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)): # takes every img in the directory appending it on a list / sorted alphabetically use 01 instead of 1
        images.append(load_image(path + '/' + img_name))
    return images