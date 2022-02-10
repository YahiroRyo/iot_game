import pygame
import copy
import json
import config
from pygame.locals import *
from block_data import BLOCKS, get_block_index_from_id
from event import KeyEvent
from context import Context

class Map(KeyEvent):
    blocks: list = []
    x = 0
    y = 0
    prev_x = 0
    prev_y = 0
    w = config.MAP_WIDTH
    h = config.MAP_HEIGHT
    is_put = False
    is_scroll = False

    def __init__(self, context: Context):
        super().__init__(context)
        if config.MAP_IS_LOAD:
            with open(f"../maps/{config.MAP_NAME}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.blocks = data["map"]
                for (idx_y, block_h) in enumerate(self.blocks):
                    for (idx_x, block_idx) in enumerate(block_h):
                        self.blocks[idx_y][idx_x] = get_block_index_from_id(block_idx)
        else:
            bg = -1
            for (idx, block) in enumerate(BLOCKS):
                if block.id == config.MAP_BG_ID:
                    bg = idx
            for _ in range(self.w):
                blocks_w = []
                for _ in range(self.h):
                    blocks_w.append(bg)
                self.blocks.append(blocks_w)
   
    def event(self, e: pygame.event.Event):
        if e.type == KEYDOWN:
            if e.key == K_s:
                out_blocks = []
                for block_h in self.blocks:
                    tmp_out_blocks = []
                    for block_idx in block_h:
                        if block_idx == -1:
                            tmp_out_blocks.append(0)
                        else:
                            tmp_out_blocks.append(BLOCKS[block_idx].id)
                    out_blocks.append(tmp_out_blocks)
                save_data = {
                    "name": config.MAP_NAME,
                    "conf": config.MAP_CONF,
                    "map": out_blocks,
                }
                with open(f"../maps/{config.MAP_NAME}.json", "w", encoding="utf-8") as f:
                    json.dump(save_data, f, ensure_ascii=False, indent=2)

        super().event(e)         
    def mouse_down_right(self, context: Context):
        (x, y) = pygame.mouse.get_pos()
        self.is_scroll = True
        self.prev_x = self.x + x
        self.prev_y = self.y + y

    def mouse_up_right(self, context: Context):
        self.is_scroll = False

    def mouse_down_left(self, context: Context):
        (x, _) = pygame.mouse.get_pos()
        if context.current_block != -1 and x >= context.get("SW") / 3:
            self.is_put = True

    def mouse_up_left(self, context: Context):
        self.is_put = False
    
    def after_event(self, context: Context):
        (x, y) = pygame.mouse.get_pos()
        if self.is_put:
            try:
                self.blocks[int((y - self.y) / config.MAP_MSIZE )][int((x - self.x - self.context.get("SW") / 3) / config.MAP_MSIZE)] = context.current_block
            except:
                pass
            
        if self.is_scroll:
            self.x = self.prev_x - x
            self.y = self.prev_y - y
    
    def draw(self):
        for (idx_y, block_h) in enumerate(self.blocks):
            for (idx_x, block_idx) in enumerate(block_h):
                if block_idx != -1:
                    block = copy.copy(BLOCKS[block_idx])
                    block.x = idx_x * config.MAP_MSIZE + self.x + self.context.get("SW") / 3
                    block.y = idx_y * config.MAP_MSIZE + self.y
                    block.draw(self.context.screen)