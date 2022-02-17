import pygame
import color
from event import KeyEvent
from canvas import Canvas
from context import Context

class UICheckbox(KeyEvent, Canvas):
    callback = None
    on_text = None
    off_text = None
    switch = False

    def __init__(self, context: Context, callback, on_text: str, off_text: str, pos: list, size: list):
        self.set_canvas(pos, size, color.BLUE)
        self.callback = callback
        font = pygame.font.Font("font/NotoSansJP-Regular.otf", 16)
        self.on_text = font.render(on_text, True, (0, 0, 0))
        self.off_text = font.render(off_text, True, (0, 0, 0))
        super().__init__(context)
    
    def mouse_down_left(self, context: Context):
        if self.is_hit():
            self.switch = not self.switch
            if self.switch:
                self.color = color.RED
            else:
                self.color = color.BLUE
            self.callback(self.switch)
    
    def draw(self):
        pygame.draw.rect(self.context.screen, self.color, (self.x, self.y, self.width, self.height))
        self.context.screen.blit(
            self.on_text if self.switch else self.off_text,
            (self.x + self.width + 10, self.y)
        )