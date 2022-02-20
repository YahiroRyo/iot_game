from map import Map
import pygame
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

def loaded_imgs():    
    Map.imgs[0] = None
    Map.imgs[1] = load_img("imgs/water.png")
    Map.imgs[2] = load_img("imgs/wall.png")
    Map.imgs[3] = load_img("imgs/rock.png")
    Map.imgs[4] = load_img("imgs/grass.png")
    Map.imgs[5] = load_img("imgs/offroad.png")
    Map.imgs[6] = load_img("imgs/blockroad.png")
    Map.imgs[7] = load_img("imgs/sand.png")
    Map.imgs[8] = load_img("imgs/deep_grass.png")
    Map.imgs[9] = load_img("imgs/water.png")
    Map.imgs[20] = load_img("imgs/light_grass_road_01.png")
    Map.imgs[21] = load_img("imgs/light_grass_road_02.png")
    Map.imgs[22] = load_img("imgs/light_grass_01.png")
    Map.imgs[23] = load_img("imgs/light_grass_02.png")
    Map.imgs[24] = load_img("imgs/light_grass_03.png")
    Map.imgs[25] = load_img("imgs/light_grass_tree_01.png")
    Map.imgs[26] = load_img("imgs/light_grass_tree_02.png")
    Map.imgs[100] = load_img("imgs/warp.png")
    Map.imgs[101] = load_img("imgs/cave.png")
    Map.imgs[102] = load_img("imgs/village.png")
    Map.imgs[103] = load_img("imgs/castle.png")
    Map.imgs[104] = load_img("imgs/stairs_up.png")
    Map.imgs[105] = load_img("imgs/stairs_down.png")
    Map.imgs[106] = load_img("imgs/tower.png")