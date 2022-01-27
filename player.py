import time
import pygame
from pygame.surface import Surface
from pygame.locals import *
from monster import Params
from map import Map
import scene as iscene
import math

# プレイヤー
class Player(Params):
    img = None
    x = 32
    y = 32
    size = 30
    speed = 1

    def __init__(self, img) -> None:
        self.img = img

    def draw(self, map: Map, screen: Surface) -> None:
        screen.blit(self.img, (self.x + map.x, self.y + map.y))

    def is_wall(self, idx: int):
        walls = [0, 1, 2]
        is_wall = False
        for wall in walls:
            if wall == idx:
                is_wall = True
        return is_wall

    def get_positions(self, key: int):
        x = 0
        y = 0
        tmp_x = 0
        tmp_y = 0
        
        if key == K_UP:
            y -= self.speed
            tmp_x = self.size
        if key == K_DOWN:
            y += self.size + self.speed
            tmp_x = self.size
        if key == K_LEFT:
            x -= self.speed
            tmp_y = self.size
        if key == K_RIGHT:
            x += self.size + self.speed
            tmp_y = self.size
        return (x, y, tmp_x, tmp_y)

    def get_keys(self):
        ret: list = []
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
           ret.append(K_UP) 
        if keys[K_DOWN]:
           ret.append(K_DOWN) 
        if keys[K_LEFT]:
           ret.append(K_LEFT) 
        if keys[K_RIGHT]:
           ret.append(K_RIGHT) 
        return ret
    
    def key_is_wall(self, key: int, map: Map):
        (x, y, tmp_x, tmp_y) = self.get_positions(key)
        return  self.is_wall(self.get_block(map, self.x + x, self.y + y)) or self.is_wall(self.get_block(map, self.x + tmp_x + x, self.y + tmp_y + y))

    def event(self, map: Map):
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            if not self.key_is_wall(K_UP, map) and self.y > 0:
                self.y -= self.speed
                map.y += self.speed
        if keys[K_DOWN]:
            if not self.key_is_wall(K_DOWN, map) and self.y < map.row * map.msize - self.size:
                self.y += self.speed
                map.y -= self.speed
        if keys[K_LEFT]:
            if not self.key_is_wall(K_LEFT, map) and self.x > 0:
                self.x -= self.speed
                map.x += self.speed
        if keys[K_RIGHT]:
            if not self.key_is_wall(K_RIGHT, map) and self.x < map.col * map.msize - self.size:
                self.x += self.speed
                map.x -= self.speed

    def get_block(self, map: Map, x: int = -1, y: int = -1):
        tmp_x = self.x if x == -1 else x
        tmp_y = self.y if y == -1 else y
        return map.map[math.floor(tmp_y / map.msize)][math.floor(tmp_x / map.msize)]

    def proc(self, map: Map, scene, scenes):
        keys = self.get_keys()
        for key in keys:
            (x, y, tmp_x, tmp_y) = self.get_positions(key)
            self_pos = self.get_block(map, self.x + x, self.y + y)
            will_pos = self.get_block(map, self.x + tmp_x, self.y + tmp_y)
            if self_pos == 0:
                # 草
                pass
            elif self_pos == 1:
                # 水
                pass
            for k in scene.conf:
                if self_pos == k or will_pos == k:
                    for i, v in enumerate(scenes.scenes):
                        if v.name == scene.conf[k][0]:
                            scenes.current_scene = i
                            self.x = scene.conf[k][1]
                            self.y = scene.conf[k][2]
                            scenes.scenes[i].map.x = (iscene.SW - (scene.conf[k][1] * 2)) / 2
                            scenes.scenes[i].map.y = (iscene.SH - (scene.conf[k][2] * 2)) / 2
                            for _ in pygame.key.get_pressed():
                                pass
                            return