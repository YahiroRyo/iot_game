import pygame
from event import KeyEvent
from context import Context
from canvas import Canvas
from block_data import BLOCKS

class Palette(KeyEvent, Canvas):
    def __init__(self, context: Context):
        super().__init__(context)
        self.set_canvas((0, 0), (context.get("SW") / 3, context.get("SH")), (255, 255, 255))
        inc = 0
        for (idx, block) in enumerate(BLOCKS):
            block.x = (idx - (inc * 10)) * 40
            block.y = inc * 40
            if 10 / ((idx - inc * 10) + 1) == 1:
                inc += 1

    def mouse_down_left(self, context: Context):
        (x, y) = pygame.mouse.get_pos()
        for (idx, block) in enumerate(BLOCKS):
            if block.is_hit(x, y):
                context.current_block = idx

    def draw(self):
        pygame.draw.rect(self.context.screen, self.color, (
                self.pos["x"],
                self.pos["y"],
                self.size["width"],
                self.size["height"]
            )
        )
        for block in BLOCKS:
            block.draw(self.context.screen)