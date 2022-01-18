from map import Map
import pygame
from pygame.locals import *


def load_img(filename, colorkey=None):
    img = pygame.image.load(filename)
    img = img.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey, RLEACCEL)
    return img

def loaded_imgs():    
    Map.imgs[0] = load_img("imgs/grass.png")
    Map.imgs[1] = load_img("imgs/water.png")
    Map.imgs[2] = load_img("imgs/wall.png")
    Map.imgs[3] = load_img("imgs/rock.png")
    Map.imgs[4] = load_img("imgs/black.png")
    Map.imgs[10] = load_img("imgs/warp.png")
    Map.imgs[11] = load_img("imgs/cave.png")