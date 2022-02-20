import pygame
import color
from event import KeyEvent
from canvas import Canvas
from context import Context

class UIRadioButton(KeyEvent, Canvas):
    callback = None
    text = None
    switch = False
    id = 0

    def __init__(self, context: Context, id: int, callback, text: str, pos: list, size: list):
        self.set_canvas(pos, size, color.BLUE)
        self.id = id
        self.callback = callback
        font = pygame.font.Font("font/NotoSansJP-Regular.otf", 16)
        self.text = font.render(text, True, (0, 0, 0))
        super().__init__(context)
    
    def mouse_down_left(self, context: Context):
        if self.is_hit():
            self.switch = not self.switch
            self.update_color()
            self.callback(self.switch, self.id)
    
    # 別のクラスからswitchフラグをいじることがあるため、色を変更するメソッドを作成した
    def update_color(self):
        if self.switch:
            self.color = color.RED
        else:
            self.color = color.BLUE
    def draw(self):
        pygame.draw.circle(self.context.screen, self.color, (self.x + self.width / 2, self.y + self.width / 2), self.width / 2)
        self.context.screen.blit(
            self.text,
            (self.x + self.width + 10, self.y)
        )