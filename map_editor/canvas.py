import pygame
from typing import Union

class Canvas:
    pos = {
        "x": 0,
        "y": 0,
    }
    size = {
        "width": 0,
        "height": 0,
    }
    color: Union[int, int, int] = (0, 0, 0)
    def set_canvas(self, pos: Union[int, int], size: Union[int, int], color:  Union[int, int, int]):
        self.pos["x"] = pos[0]
        self.pos["y"] = pos[1]
        self.size["width"] = size[0]
        self.size["height"] = size[1]
        self.color = color
    
    def is_hit(self) -> bool:
        (x, y) = pygame.mouse.get_pos()
        return  self.pos["x"] <= x                 and \
                self.pos["x"] + self.size["width"] >= x   and \
                self.pos["y"] <= y                 and \
                self.pos["y"] + self.size["height"] >= y