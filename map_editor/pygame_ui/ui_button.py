import pygame
from event import KeyEvent
from canvas import Canvas
from context import Context

class UIButton(KeyEvent, Canvas):
    callback = None
    draw_text = None
    text = ""

    def __init__(self, context: Context, callback, text: str, pos: list, size: list, color: list):
        self.text = text
        self.set_canvas(pos, size, color)
        font = pygame.font.Font("font/NotoSansJP-Regular.otf", 16)
        self.draw_text = font.render(text, True, (255, 255, 255))
        self.callback = callback
        super().__init__(context)
    
    def mouse_down_left(self, context: Context):
        if self.is_hit():
            self.callback()
    
    def draw(self):
        pygame.draw.rect(self.context.screen, self.color, (self.x, self.y, self.width, self.height))
        self.context.screen.blit(
            self.draw_text,
            (self.x - self.draw_text.get_width() / 2 + self.width / 2, self.y - self.draw_text.get_height() / 2 + self.height / 2)
        )