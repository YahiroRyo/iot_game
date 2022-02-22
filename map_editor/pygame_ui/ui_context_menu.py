import pygame
import color
from event import KeyEvent
from canvas import Canvas
from context import Context

class UIContextMenu(KeyEvent, Canvas):
    uis = []
    stack = []
    is_active = False
    prev_x = 0
    prev_y = 0
    
    def __init__(self, context: Context, uis: list):
        super().__init__(context)
        self.uis = uis
        self.set_canvas((0, 0), (24 * 10 + 20, sum([ui.height for ui in uis]) + 20), color.WHITE)

    def event(self, e: pygame.event.Event):
        super().event(e)
        if self.is_active:
            for ui in self.uis:
                ui.event(e)

    def mouse_down_right(self, context: Context):
        (self.prev_x, self.prev_y) = pygame.mouse.get_pos()

    def mouse_up_right(self, context: Context):
        (self.x, self.y) = pygame.mouse.get_pos()
        if self.x == self.prev_x and self.y == self.prev_y:
            self.is_active = True
            sum_height = 0
            for idx, ui in enumerate(self.uis):
                ui.set_pos(self.x + 10, self.y + ((idx + 1) * 10) + sum_height)
                sum_height += ui.height
        else:
            self.is_active = False
    
    def mouse_down_left(self, context: Context):
        if not self.is_hit():
            self.is_active = False

    def draw(self):
        if self.is_active:
            pygame.draw.rect(self.context.screen, self.color, (self.x, self.y, self.width, self.height))
            for ui in self.uis:
                ui.draw()

    def push(self, uis: list):
        tmp_uis = []
        for (idx, ui) in enumerate(uis):
            tmp_uis.append(len(self.uis) + idx)
        self.stack.append(tmp_uis)
        self.uis.extend(uis)
        self.set_canvas((0, 0), (24 * 10 + 20, sum([ui.height for ui in self.uis]) + len(self.uis) * 15), color.WHITE)

    def pop(self):
        stack = self.stack.pop(0)
        tmp_uis = []
        for idx in stack:
            tmp_uis.append(self.uis[idx])
        for ui in tmp_uis:
            self.uis.remove(ui)
        self.set_canvas((0, 0), (24 * 10 + 20, sum([ui.height for ui in self.uis]) + 20), color.WHITE)