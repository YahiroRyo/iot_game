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
    Map.imgs[0] = None
    Map.imgs[1] = load_img("imgs/water.png")
    Map.imgs[2] = load_img("imgs/wall.png")
    Map.imgs[3] = load_img("imgs/rock.png")
    Map.imgs[4] = load_img("imgs/grass.png")
    Map.imgs[5] = load_img("imgs/offroad.png")
    Map.imgs[6] = load_img("imgs/blockroad.png")
    Map.imgs[7] = load_img("imgs/sand.png")
    Map.imgs[100] = load_img("imgs/warp.png")
    Map.imgs[101] = load_img("imgs/cave.png")
    Map.imgs[102] = load_img("imgs/village.png")
    Map.imgs[103] = load_img("imgs/castle.png")
    Map.imgs[104] = load_img("imgs/stairs_up.png")
    Map.imgs[105] = load_img("imgs/stairs_down.png")