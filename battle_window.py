from pygame import Surface
from window import Window
from typing import Tuple
import scene

MARGIN = 10
class BattleStatusWindow(Window):
    def event(self) -> Tuple[bool, bool, dict]:
        return super().event()

    def draw(self, screen: Surface, x: int, name: str, hp: int = 0, mp: int = 0, maxhp: int = 0, maxmp: int = 0):
        self._draw(screen, scene.SW / 4 - MARGIN * 2, 32 * 3, x + MARGIN, MARGIN)
        self._draw_str(screen, f"{name}\nHP: {hp}/{maxhp}\nMP: {mp}/{maxmp}")