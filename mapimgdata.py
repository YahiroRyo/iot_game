import pygame
import os
from map import Map
from pygame.locals import *

def load_img(filename, colorkey=None, resize=True):
    img = pygame.image.load(filename)
    if resize:
        img = pygame.transform.scale(img, (32, 32))
    img = img.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey, RLEACCEL)
    return img

FILTER = [
    "character",
    "monsters",
    "titleicon.png",
]

def loaded_imgs():
    files = os.listdir("imgs")
    for filter in FILTER:
        files.remove(filter)

    Map.imgs[0] = None
    for file in files:
        names = file.split("_")
        Map.imgs[int(names[0])] = load_img(f"imgs/{file}")