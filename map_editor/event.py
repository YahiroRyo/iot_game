import pygame
from pygame.locals import *
from context import Context

class KeyEvent:
    context: Context

    def __init__(self, context: Context):
        self.context = context

    def event(self, e: pygame.event.Event):
        if e.type == MOUSEBUTTONDOWN:
            # 左クリック
            if e.button == self.context.get("ML"):
                self.mouse_down_left(self.context)
            # ホイールクリック
            if e.button == self.context.get("MM"):
                self.mouse_down_middle(self.context)
            # 右クリック
            if e.button == self.context.get("MR"):
                self.mouse_down_right(self.context)
        if e.type == MOUSEBUTTONUP:
            # 左クリック
            if e.button == self.context.get("ML"):
                self.mouse_up_left(self.context)
            # ホイールクリック
            if e.button == self.context.get("MM"):
                self.mouse_up_middle(self.context)
            # 右クリック
            if e.button == self.context.get("MR"):
                self.mouse_up_right(self.context)
        self.after_event(self.context)
    
    def mouse_down_left(self, context: Context):
        pass
    def mouse_down_middle(self, context: Context):
        pass
    def mouse_down_right(self, context: Context):
        pass

    def mouse_up_left(self, context: Context):
        pass
    def mouse_up_middle(self, context: Context):
        pass
    def mouse_up_right(self, context: Context):
        pass

    def after_event(self, context: Context):
        pass