import pygame
from context import Context
pygame.init()
context = Context()
screen = pygame.display.set_mode((context.get("SW"), context.get("SH")))

from map import Map

map = Map(context)
context.map = map
context.screen = screen

import sys
from palette import Palette
from pygame.locals import *

def draw():
    pygame.Surface.fill(screen, (0, 0, 0))
    map.draw()
    palette.draw()
    pygame.display.update()
    clock.tick(context.get("FPS"))

def event():
    for e in pygame.event.get():
        if e.type == QUIT:          # 閉じるボタンが押されたとき
            pygame.quit()
            sys.exit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:   # Escキーが押されたとき
                pygame.quit()
                sys.exit()
        map.event(e)
        palette.event(e)

clock = pygame.time.Clock()
palette = Palette(context)

while True:
    draw()
    event()