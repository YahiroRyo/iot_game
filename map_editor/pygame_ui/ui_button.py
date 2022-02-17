import pygame
from event import KeyEvent
from canvas import Canvas
from context import Context

class UIButton(KeyEvent, Canvas):
    callback = None
    text = ""

    def __init__(self, context: Context, callback, text: str, pos: list, size: list, color: list):
        self.text = text
        self.set_canvas(pos, size, color)
        self.callback = callback
        super().__init__(context)
    
    def mouse_down_left(self, context: Context):
        if self.is_hit():
            self.callback()
    
    def draw(self):
        pygame.draw.rect(self.context.screen, self.color, (self.x, self.y, self.width, self.height))
    