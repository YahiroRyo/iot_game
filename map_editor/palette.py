import pygame
from event import KeyEvent
from context import Context
from canvas import Canvas
from block_data import BLOCKS

class Palette(KeyEvent, Canvas):
    def __init__(self, context: Context):
        super().__init__(context)
        self.set_canvas((0, 0), (context.get("SW") / 3, context.get("SH")), (255, 255, 255))
        sum_idx = 0
        for (idx, block) in enumerate(BLOCKS):
            block.x = (idx - sum_idx) * 40
            block.y = int((idx * 40) / (context.get("SW") / 3.2)) * 40
            sum_idx += int((context.get("SW") / 2.9) / 40) if int(((idx - sum_idx) * 40) / (context.get("SW") / 3.2)) else 0

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