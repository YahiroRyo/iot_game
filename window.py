from pygame.surface import Surface
import pygame
import color

class Window:
    _w = 0
    _h = 0
    _x = 0
    _y = 0
    
    def _draw(self, screen: Surface, width: int, height: int, x: int, y: int):
        pygame.draw.rect(screen, color.WHITE, (x, y, width, height), 5)
        pygame.draw.rect(screen, color.BLACK, (x + 5, y + 5, width - 10, height - 10))
        self._w = width
        self._h = height
        self._x = x
        self._y = y

    def _draw_str(self, screen: Surface, string: str, color = color.ORANGE, font_size: int = 32):
        font = pygame.font.SysFont(None, font_size)
        text = font.render(string, True, color)
        screen.blit(text, (self._x + 10, self._y + 10))