import pygame
import config
import json
from context import Context
pygame.init()
context = Context()
screen = pygame.display.set_mode((context.get("SW"), context.get("SH")))

from layer import Layer

layer = Layer(context)
context.layer = layer
context.screen = screen

import sys
from palette import Palette
from pygame.locals import *
from ui import UI

ui = UI(context)

def draw():
    pygame.Surface.fill(screen, (0, 0, 0))
    layer.draw()
    palette.draw()
    ui.draw()
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
            if e.type == KEYDOWN:   # save処理
                if e.key == K_s:
                    maps = {
                        "map_main": [],
                        "map_everything": [],
                        "map_npcs": [],
                    }

                    for (idx, key) in enumerate(maps):
                        blocks = []
                        if idx == 0: blocks = layer.map.blocks
                        if idx == 1: blocks = layer.everything.blocks
                        if idx == 2: blocks = layer.npcs.blocks
                        for block_h in blocks:
                            tmp_out_blocks = []
                            for block_idx in block_h:
                                if block_idx == -1:
                                    tmp_out_blocks.append(0)
                                else:
                                    tmp_out_blocks.append(context.get("BLOCKS")[block_idx].id)
                            maps[key].append(tmp_out_blocks)
                    save_data = dict({
                        "name": config.MAP_NAME,
                        "conf": config.MAP_CONF,
                        "events": context.events
                    }, **maps)
                    with open(f"../maps/{config.MAP_NAME}.json", "w", encoding="utf-8") as f:
                        json.dump(save_data, f, ensure_ascii=False, indent=2)
        layer.event(e)
        palette.event(e)
        ui.event(e)

clock = pygame.time.Clock()
palette = Palette(context)

while True:
    draw()
    event()