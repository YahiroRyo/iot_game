import color
import pygame
from event import KeyEvent
from canvas import Canvas
from context import Context

class UIContextMenuRadioButton(KeyEvent, Canvas):
    id = 0
    callback = None
    on_text = None
    off_text = None
    switch = False
    
    def __init__(self, context: Context, callback, on_text: str, off_text: str, id: int):
        super().__init__(context)
        self.callback = callback
        font = pygame.font.Font("font/NotoSansJP-Regular.otf", 16)
        self.on_text = font.render(on_text, True, (0, 0, 0))
        self.off_text = font.render(off_text, True, (0, 0, 0))
        self.set_canvas((0, 0), (24 * 10, 32), color.BLUE)
        self.id = id

    def mouse_down_left(self, context: Context):
        if self.is_hit():
            self.switch = not self.switch
            self.update_color()
            self.callback(self.switch, self.id)

    def update_color(self):
        if self.switch:
            self.color = color.RED
        else:
            self.color = color.BLUE
    
    def draw(self):
        if self.is_hit():
            pygame.draw.rect(self.context.screen, color.DEEP_WHITE, (self.x, self.y, self.width, self.height))
        pygame.draw.circle(self.context.screen, self.color, (self.height / 2 + self.x, self.height / 2 + self.y), self.height / 2)
        self.context.screen.blit(
            self.on_text if self.switch else self.off_text,
            (self.x + self.height + 10, self.y)
        )