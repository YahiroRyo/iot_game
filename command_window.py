import window
import pygame
import scene
import color
from pygame.surface import Surface
from command import Command, command_select
from pygame.locals import *
from typing import Tuple

COOL_TIME = 20

class CommandWindow(window.Window):
    command_term_cnt = []
    commands = []
    is_operate = False
    unique_name = ""
    selected = 0

    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self, cmd_num: Command, w = 0, h = 0, x = 0, y = 0) -> None:
        super().__init__()
        self.set_commands(cmd_num)
        self.width = w if w != 0 else scene.SW - 50
        self.height = h if h != 0 else scene.SH / 3
        self.x = x if x != 0 else 25
        self.y = y if y != 0 else scene.SH - scene.SH / 3 - 25

    # コマンドをセットできる selectedは0に初期化される
    def set_commands(self, cmd_num: Command = Command.NONE, unique_name: str = "", command_msgs: list = []):
        self.selected = 0
        if cmd_num == Command.NONE:
            self.commands = command_msgs
            self.unique_name = unique_name
            self.command_term_cnt = [0]
            sum = 0
            for i in range(1, len(command_msgs)):
                sum += len(command_msgs[i - 1]) + 1
                self.command_term_cnt.append(sum)
        else:
            (self.unique_name, self.commands, self.command_term_cnt) = command_select(cmd_num)

    # コマンド描画
    def draw(self, screen: Surface):
        self._draw(
            screen,
            self.width,
            self.height,
            self.x,
            self.y,
        )
        msg = "  "
        for command in self.commands:
            msg += command + "  "
        self._draw_str(screen, msg)
        self.command_select(screen, command_term_cnt = self.command_term_cnt, selected = self.selected)

    # コマンド操作
    def event(self) -> Tuple[bool, bool, dict]:
        if self.cool_time <= 0:
            keys = pygame.key.get_pressed()
            if keys[K_RIGHT] and self.selected < len(self.commands)-1:
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

    # コマンドの矢印を動かす
    def command_select(self, screen: Surface, color = color.ORANGE, command_term_cnt: list = [], selected: int = 0):
        select_x = command_term_cnt[selected] * 24
        select_y = 0
        text = self.font.render("→", True, color)
        screen.blit(text, (self._x + 10+ select_x, self._y + 10 + select_y))