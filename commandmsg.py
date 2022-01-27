import window
import pygame
from pygame.surface import Surface
import scene
import command
from pygame.locals import *
from typing import Tuple


class CommandWindow(window.Window):
    commandactive = True
    msgwordcount = []
    msgs = []
    is_operate = False
    selected = 0

    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self, msgnum: int, w = 0, h = 0, x = 0, y = 0) -> None:
        super().__init__()
        (self.msgs, self.msgwordcount) = command.command_select(msgnum)
        self.is_operate = False
        self.width = w if w != 0 else scene.SW - 50
        self.height = h if h != 0 else scene.SH / 3
        self.x = x if x != 0 else 25
        self.y = y if y != 0 else scene.SH - scene.SH / 3 - 25

    def draw(self, screen: Surface):
        self._draw(
            screen,
            self.width,
            self.height,
            self.x,
            self.y,
        )
        msg = "  "
        for lenmsg in self.msgs:
            msg += lenmsg+"  "
        self._draw_str(screen, msg)
        self.command_select(screen, msgs_cnt=self.msgwordcount, selected=self.selected)

    def event(self) -> Tuple[bool, bool, dict]:
        if self.cool_time <= 0:
            keys = pygame.key.get_pressed()
            if keys[K_RIGHT] and self.selected < len(self.msgs)-1:
                self.selected += 1
            elif keys[K_LEFT] and self.selected > 0:
                self.selected -= 1
            elif keys[K_RETURN]:
                return (self.is_operate, True, {
                    "msg": self.msgs[self.selected]
                })
        else:
            self.cool_time -= 1
        return (self.is_operate, False, {})
