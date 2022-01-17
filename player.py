import pygame
from pygame.event import Event
from pygame.surface import Surface
from pygame.locals import *
from map import Map
import math

# プレイヤー
class Player:
    img = None
    x = 10
    y = 10
    speed = .05

    def __init__(self, img) -> None:
        self.img = img

    def draw(self, screen: Surface) -> None:
        screen.blit(self.img, (self.x, self.y))

    def is_wall(self, idx: int):
        walls = [2,4]
        is_wall = False
        for wall in walls:
            if wall == idx:
                is_wall = True
        return is_wall

    def event(self, map: Map):
        keys = pygame.key.get_pressed()
        (idx, wx, wy) = self.get_block(map)
        is_wall = self.is_wall(idx)
        if keys[K_UP]:
            self.y -= self.speed
            if is_wall or self.y < 0:
                self.y += self.speed + 1
        elif keys[K_DOWN]:
            self.y += self.speed
            if is_wall or self.y > map.row * map.msize - 31:
                self.y -= self.speed + 1
        elif keys[K_LEFT]:
            self.x -= self.speed
            if is_wall or self.x < 0:
                self.x += self.speed + 1
        elif keys[K_RIGHT]:
            self.x += self.speed
            if is_wall or self.x > map.col* map.msize - 31:
                self.x -= self.speed + 1

    def get_block(self, map: Map):
        return (map.map[math.floor(self.y / map.msize)][math.floor(self.x / map.msize)], math.floor(self.x / map.msize) * map.msize, math.floor(self.y / map.msize) * map.msize)

    def proc(self, map: Map, scene, scenes):
        (idx, wx, wy) = self.get_block(map)
        if idx == 0:
            # 草
            pass
        elif idx == 1:
            # 水
            pass
        for k in scene.conf:
            if idx == k:
                for i, v in enumerate(scenes.scenes):
                    if v.name == scene.conf[k][0]:
                        scenes.current_scene = i
                        self.x = scene.conf[k][1]
                        self.y = scene.conf[k][2]
                        return