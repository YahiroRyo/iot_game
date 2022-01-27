from pygame.surface import Surface
from typing import Tuple
import pygame
import color

class Window:
    _w = 0
    _h = 0
    _x = 0
    _y = 0
    font = None
    cool_time = 10

    def _draw(self, screen: Surface, width: int, height: int, x: int, y: int):
        pygame.draw.rect(screen, color.WHITE, (x, y, width, height), 5)
        pygame.draw.rect(screen, color.BLACK, (x + 5, y + 5, width - 10, height - 10))
        self._w = width
        self._h = height
        self._x = x
        self._y = y
        self.font = pygame.font.Font("fonts/PixelMplus10-Regular.ttf", 24)

    def _draw_str(self, screen: Surface, string: str, color = color.ORANGE):
        strings = string.split("\n")
        for idx, s in enumerate(strings):
            text = self.font.render(s, True, color)
            screen.blit(text, (self._x + 10, self._y + 10 + (idx * 24)))
    
    # 返り値
    # 1: 操作権限
    # 2: 閉じたか
    # 3: その他のデータ
    def event(self) -> Tuple[bool, bool, dict]:
        pass

    def command_select(self, screen: Surface, color = color.ORANGE, msgs_cnt: list = [], selected: int=0):
        select_x = msgs_cnt[selected]*24
        select_y = 0
        text = self.font.render("→", True, color)
        screen.blit(text, (self._x + 10+ select_x, self._y + 10 + select_y))