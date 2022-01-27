import window
import pygame
from pygame.surface import Surface
import scene
import command
from pygame.locals import *
from typing import Tuple

COOL_TIME = 20

class CommandWindow(window.Window):
    commandactive = True
    msgwordcount = []
    msgs = []
    is_operate = False
    unique_name = ""
    selected = 0

    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self, msgnum: int, w = 0, h = 0, x = 0, y = 0) -> None:
        super().__init__()
        (self.unique_name, self.msgs, self.msgwordcount) = command.command_select(msgnum)
        self.is_operate = False
        self.width = w if w != 0 else scene.SW - 50
        self.height = h if h != 0 else scene.SH / 3
        self.x = x if x != 0 else 25
        self.y = y if y != 0 else scene.SH - scene.SH / 3 - 25

    # コマンドをセットできる selectedは0に初期化される
    def set_commands(self, msgnum: int = 0, unique_name: str = "", command_msgs: list = []):
        self.selected = 0
        if msgnum == 0:
            self.msgs = command_msgs
            self.unique_name = unique_name
            self.msgwordcount = [0]
            sum = 0
            for i in range(1, len(command_msgs)):
                sum += len(command_msgs[i - 1]) + 1
                self.msgwordcount.append(sum)
        else:
            (self.unique_name, self.msgs, self.msgwordcount) = command.command_select(msgnum)

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
                self.cool_time = COOL_TIME
                self.selected += 1
            elif keys[K_LEFT] and self.selected > 0:
                self.cool_time = COOL_TIME
                self.selected -= 1
            elif keys[K_RETURN]:
                self.cool_time = COOL_TIME
                return (self.is_operate, True, {
                    "unique": self.unique_name,
                    "index": self.selected
                })
        else:
            self.cool_time -= 1
        return (self.is_operate, False, {})
