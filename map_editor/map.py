import pygame
import copy
import config
from pygame.locals import *
from block_data import BLOCKS, get_block_index_from_id
from event import KeyEvent
from context import Context

class Map(KeyEvent):
    blocks: list = []
    w = config.MAP_WIDTH
    h = config.MAP_HEIGHT
    x = 0
    y = 0

    def __init__(self, context: Context, blocks: list):
        super().__init__(context)
        self.blocks = blocks
   
    def event(self, e: pygame.event.Event):
        super().event(e)
    
    def draw(self):
        for (idx_y, block_h) in enumerate(self.blocks):
            for (idx_x, block_idx) in enumerate(block_h):
                if block_idx != -1:
                    block = copy.copy(BLOCKS[block_idx])
                    block.x = idx_x * config.MAP_MSIZE + self.x + self.context.get("SW") / 3
                    block.y = idx_y * config.MAP_MSIZE + self.y
                    block.draw(self.context.screen)