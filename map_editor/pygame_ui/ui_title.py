import pygame
from canvas import Canvas
from context import Context

class UITitle(Canvas):
    context: Context = None
    title = None

    def __init__(self, context: Context, title: str, pos: list, color: list):
        self.context = context
        self.set_canvas(pos, (32, 32), color)
        font = pygame.font.Font("font/NotoSansJP-Regular.otf", 32)
        self.title = font.render(title, True, color)
    
    def mouse_down_left(self, context: Context):
        if self.is_hit():
            self.callback()
    
    def draw(self):
        self.context.screen.blit(
            self.title,
            (self.x, self.y)
        )