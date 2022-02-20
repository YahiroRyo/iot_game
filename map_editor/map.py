import pygame
import copy
import config
from pygame.locals import *
from block_data import BLOCKS
from event import KeyEvent
from context import Context

class Map(KeyEvent):
    blocks: list = []
    tmp_blocks: list = []
    w = config.MAP_WIDTH
    h = config.MAP_HEIGHT
    x = 0
    y = 0

    def __init__(self, context: Context, blocks: list):
        super().__init__(context)
        self.blocks = blocks
        self.update_blocks()
   
    def event(self, e: pygame.event.Event):
        super().event(e)

    def draw(self):
        self.update_blocks_pos()
        for block_h in self.tmp_blocks:
            for block in block_h:
                if block.id != 0:
                    block.draw(self.context.screen)

    def update_blocks_pos(self):
        for (idx_y, block_h) in enumerate(self.tmp_blocks):
            for (idx_x, block) in enumerate(block_h):
                block.x =  idx_x * config.MAP_MSIZE + self.x + self.context.get("SW") / 3
                block.y = idx_y * config.MAP_MSIZE + self.y

    def update_blocks(self):
        self.tmp_blocks = []
        for (idx_y, block_h) in enumerate(self.blocks):
            tmp_blocks_w = []
            for (idx_x, block_idx) in enumerate(block_h):
                if block_idx != -1:
                    block = copy.copy(BLOCKS[block_idx])
                    block.x = idx_x * config.MAP_MSIZE + self.x + self.context.get("SW") / 3
                    block.y = idx_y * config.MAP_MSIZE + self.y
                    tmp_blocks_w.append(block)
                else:
                    tmp_blocks_w.append(BLOCKS[0])
            self.tmp_blocks.append(tmp_blocks_w)