import pygame
from pygame.surface import Surface
from window import Window
from pygame.locals import *
from typing import Tuple
import scene

class Message(Window):
    msg = ""
    is_operate = False

    def __init__(self, msg: str, is_operate: bool) -> None:
        super().__init__()
        self.msg = msg
        self.is_operate = is_operate

    def draw(self, screen: Surface):
        self._draw(
            screen,
            scene.SW - 50,
            scene.SH / 3,
            25,
            scene.SH - scene.SH / 3 - 25
        )
        self._draw_str(screen, self.msg)

    def draw_until_press_key(self, screen: Surface):
        while True:
            self._draw(
                screen,
                scene.SW - 50,
                scene.SH / 3,
                25,
                scene.SH - scene.SH / 3 - 25
            )
            self._draw_str(screen, self.msg)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return

    def event(self) -> Tuple[bool, bool, dict]:
        if self.cool_time <= 0:
            keys = pygame.key.get_pressed()
            if keys[K_RETURN]:
                return (self.is_operate, True, {})
        else:
            self.cool_time -= 1
        return (self.is_operate, False, {})