import pygame
import pyperclip
from pygame.locals import *
from event import KeyEvent
from canvas import Canvas
from context import Context

KEYS = [
    {
        "key": K_0,
        "text": "0",
    },
    {
        "key": K_1,
        "text": "1",
    },
    {
        "key": K_2,
        "text": "2",
    },
    {
        "key": K_3,
        "text": "3",
    },
    {
        "key": K_4,
        "text": "4",
    },
    {
        "key": K_5,
        "text": "5",
    },
    {
        "key": K_6,
        "text": "6",
    },
    {
        "key": K_7,
        "text": "7",
    },
    {
        "key": K_8,
        "text": "8",
    },
    {
        "key": K_9,
        "text": "9",
    },
    {
        "key": K_SPACE,
        "text": " ",
    },
]

class UIInput(KeyEvent, Canvas):
    is_input = False
    font = None
    text = ""
    cool_time = 10
    title = None

    def __init__(self, context: Context, pos: list, width: int, title: str):
        super().__init__(context)
        self.set_canvas(pos, (width, 32), (0, 0, 0))
        self.font = pygame.font.Font("font/NotoSansJP-Regular.otf", 24)
        title_font = pygame.font.Font("font/NotoSansJP-Regular.otf", 16)
        self.title = title_font.render(title, True, (0, 0, 0))
    
    def event(self, e: pygame.event.Event):
        super().event(e)
        self.cool_time -= 1 if self.cool_time != 0 else 0 
        if self.is_input:
            keys = pygame.key.get_pressed()
            if (keys[K_LCTRL] or keys[K_RCTRL]) and keys[K_v] and self.cool_time == 0:
                self.text += pyperclip.paste()
                self.cool_time = 10
            if e.type == KEYDOWN:
                for key in KEYS:
                    if e.key == key["key"]:
                        self.text += key["text"]
                if e.key == K_BACKSPACE:
                    self.text = self.text[:-1]
    
    def draw(self):
        pygame.draw.rect(
            self.context.screen,
            (255, 255, 255),
            (self.x, self.y, self.width, self.height),
        )
        pygame.draw.rect(
            self.context.screen,
            (0, 0, 0),
            (self.x, self.y, self.width, self.height),
            2
        )
        text = self.font.render(self.text, True, (0, 0, 0))
        self.context.screen.blit(
            text,
            (self.x, self.y)
        )
        self.context.screen.blit(
            self.title,
            (self.x, self.y - 24)
        )
        if self.is_input:
            pygame.draw.rect(
                self.context.screen,
                (0, 0, 0),
                (self.x + 8 + text.get_width(), self.y + 4, 8, self.height - 8)
            )
    
    def mouse_down_left(self, context: Context):
        if self.is_hit():
            self.is_input = True
        else:
            self.is_input = False
    
    def reset_text(self):
        self.text = ""