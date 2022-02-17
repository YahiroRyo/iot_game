import pygame
from typing import Union

class Canvas:
    x = 0
    y = 0
    width = 0
    height = 0
    color: list = (0, 0, 0)
    def set_canvas(self, pos: list, size: list, color:  list):
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.color = color
    
    def is_hit(self) -> bool:
        (x, y) = pygame.mouse.get_pos()
        return  self.x <= x                 and \
                self.x + self.width >= x   and \
                self.y <= y                 and \
                self.y + self.height >= y