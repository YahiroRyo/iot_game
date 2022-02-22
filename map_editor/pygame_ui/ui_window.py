import pygame
from event import KeyEvent
from canvas import Canvas
from context import Context
from pygame_ui.ui_button import UIButton

MARGIN = 5

class UIWindow(KeyEvent, Canvas):
    close_button: UIButton = None
    submit_button: UIButton = None
    uis = []
    title = None
    close_callback = None
    submit_callback = None
    
    def __init__(self, context: Context, title: str, pos: list, size: list, uis: list, close_callback, submit_callback):
        super().__init__(context)
        self.set_canvas(pos, size, (255, 255, 255))
        self.init(uis, title)
        self.close_button = UIButton(
            context,
            self.close,
            "x",
            (pos[0] + size[0] - 32 - MARGIN, pos[1] + MARGIN),
            (32, 32),
            (255, 0, 0)
        )
        self.submit_button = UIButton(
            context,
            self.submit,
            "決定",
            (pos[0] + MARGIN, pos[1] + size[1] - 32 - MARGIN),
            (100, 32),
            (150, 150, 150)
        )
        self.submit_callback = submit_callback
        self.close_callback = close_callback
    
    def draw(self):
        pygame.draw.rect(
            self.context.screen,
            (255, 255, 255),
            (self.x, self.y, self.width, self.height)
        )
        self.context.screen.blit(
            self.title,
            (self.x + MARGIN, self.y + MARGIN)
        )
        for ui in self.uis:
            ui.draw()
        self.submit_button.draw()
        self.close_button.draw()

    def event(self, e: pygame.event.Event):
        super().event(e)
        for ui in self.uis:
            ui.event(e)
        self.close_button.event(e)
        self.submit_button.event(e)

    def set_title(self, title):
        font = pygame.font.Font("font/NotoSansJP-Regular.otf", 16)
        self.title = font.render(title, True, (0, 0, 0))

    def set_uis(self, uis: list):
        self.uis = uis
    
    def init(self, uis: list, title: str):
        self.set_uis(uis)
        self.set_title(title)

    def submit(self):
        self.submit_callback(self.uis)

    def close(self):
        self.close_callback()