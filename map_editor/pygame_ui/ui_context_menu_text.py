import color
import pygame
from event import KeyEvent
from canvas import Canvas
from context import Context

class UIContextMenuText(KeyEvent, Canvas):
    font = None
    text = "None"
    
    def __init__(self, context: Context, text: str):
        super().__init__(context)
        self.font = pygame.font.Font("font/NotoSansJP-Regular.otf", 16)
        self.text = text
        self.height = 20

    def draw(self):
        text = self.font.render(self.text, True, (0, 0, 0))
        self.context.screen.blit(
            text,
            (self.x, self.y)
        )