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
    
    def draw_status(self, screen: Surface, player, x: int):
        self._draw(screen, scene.SW / 4 - MARGIN * 2, 32 * 8 + MARGIN, x + MARGIN, MARGIN)
        self._draw_str(screen, f"　職　業　: {player.name}\n　Ｈ　Ｐ　: {player.hp}/{player.maxhp}\n　Ｍ　Ｐ　: {player.mp}/{player.maxmp}\n攻　撃　力: {player.power}\n防　御　力: {player.defense}\n魔法攻撃力: {player.m_power}\n魔法防御力: {player.m_defense}\n素　早　さ: {player.agility}\n　会　心　: {player.luck}\n経　験　値: {player.exp}")