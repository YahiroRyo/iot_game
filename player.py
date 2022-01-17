import pygame
from pygame.event import Event
from pygame.surface import Surface
from pygame.locals import *
from map import Map
import math

# プレイヤー
class Player:
    img = None
    x = 32
    y = 32
    speed = .05

    def __init__(self, img) -> None:
        self.img = img

    def draw(self, map: Map, screen: Surface) -> None:
        screen.blit(self.img, (self.x + map.x, self.y + map.y))

    def is_wall(self, idx: int):
        walls = [1, 2, 4]
        is_wall = False
        for wall in walls:
            if wall == idx:
                is_wall = True
        return is_wall

    def key_is_wall(self, key: int, map: Map):
        x = 0
        y = 0
        if key == K_UP:
            y = -self.speed
        if key == K_DOWN:
            y = self.speed
        if key == K_LEFT:
            x = -self.speed
        if key == K_RIGHT:
            x = self.speed
        id = map.map[math.floor((self.y + y) / map.msize)][math.floor((self.x + x) / map.msize)]
        return self.is_wall(id)

    def event(self, map: Map):
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            if not self.key_is_wall(K_UP, map) and self.y > 0: self.y -= self.speed
        if keys[K_DOWN]:
            if not self.key_is_wall(K_DOWN, map) and self.y < map.row * map.msize - 31: self.y += self.speed
        if keys[K_LEFT]:
            if not self.key_is_wall(K_LEFT, map) and self.x > 0: self.x -= self.speed
        if keys[K_RIGHT]:
            if not self.key_is_wall(K_RIGHT, map) and self.x < map.col * map.msize - 31: self.x += self.speed

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