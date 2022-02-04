from distutils import command
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
    command_term_cnts = []
    commands = []
    is_operate = False
    unique_name = ""
    selected = 0

    x = 0
    y = 0
    width = 0
    height = 0
    page_cnt = 0

    def __init__(self, cmd_num: Command, w = 0, h = 0, x = 0, y = 0) -> None:
        super().__init__()
        self.set_commands(cmd_num)
        self.width = w if w != 0 else scene.SW - 50
        self.height = h if h != 0 else scene.SH / 3
        self.x = x if x != 0 else 25
        self.y = y if y != 0 else scene.SH - scene.SH / 3 - 25

    # コマンドをセットできる selectedは0に初期化される
    def set_commands(self, cmd_num: Command = Command.NONE, unique_name: str = "", tmp_commands: list = []):
        self.selected = 0
        if cmd_num == Command.NONE:
            self.commands = []
            self.unique_name = unique_name
            self.command_term_cnts = []

            command_term_cnt = [0]
            tmp_command = []
            sum = 0
            for tmp_cmd in tmp_commands:
                sum += len(tmp_cmd) + 1
                tmp_command.append(tmp_cmd)
                command_term_cnt.append(sum)
                if sum * 24 + (len(tmp_cmd) - 1) * 24 >= scene.SW:
                    sum = 0
                    self.command_term_cnts.append(command_term_cnt)
                    self.commands.append(tmp_command)
                    command_term_cnt = [0]
                    tmp_command = []
            command_term_cnt.pop()
            self.command_term_cnts.append(command_term_cnt)
            self.commands.append(tmp_command)
        else:
            (self.unique_name, self.commands, self.command_term_cnts) = command_select(cmd_num)

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
        for command in self.commands[self.page_cnt]:
            msg += command + "  "
        self._draw_str(screen, msg)
        self.command_select(screen, command_term_cnts = self.command_term_cnts[self.page_cnt], selected = self.selected)

    # コマンド操作
    def event(self) -> Tuple[bool, bool, dict]:
        if self.cool_time <= 0:
            keys = pygame.key.get_pressed()
            if keys[K_RIGHT]:
                self.cool_time = COOL_TIME
                if self.selected >= len(self.commands[self.page_cnt]) - 1:
                    if len(self.commands) - 1 < self.page_cnt + 1:
                        self.page_cnt = 0
                    else:
                        self.page_cnt += 1
                    self.selected = 0
                else:
                    self.selected += 1
            elif keys[K_LEFT]:
                self.cool_time = COOL_TIME
                if self.selected == 0:
                    # なんか変だぞお????!!!!!!!
                    if self.page_cnt == 0:
                        self.page_cnt = len(self.command_term_cnts) - 1
                        self.selected = len(self.command_term_cnts[len(self.command_term_cnts) - 1]) - 2
                    else:
                        self.page_cnt -= 1
                        self.selected = len(self.command_term_cnts[self.page_cnt]) - 2
                else:
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
    def command_select(self, screen: Surface, color = color.ORANGE, command_term_cnts: list = [], selected: int = 0):
        select_x = command_term_cnts[selected] * 24
        select_y = 0
        text = self.font.render("→", True, color)
        screen.blit(text, (self._x + 10+ select_x, self._y + 10 + select_y))