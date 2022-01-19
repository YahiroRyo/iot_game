from distutils import command
from time import time
import window
import pygame
from pygame.surface import Surface
import scene
import command
from pygame.locals import *


class CommandWindow(window.Window):

    commandactive=True
    msgwordcount = []
    lenmsgs = []
    msgcommand= []
    is_operate = False
    selected=0

    def __init__(self, msgnum :int) -> None:
        super().__init__()
        (self.lenmsgs,self.msgcommand,self.msgwordcount) = command.command_select(msgnum)
        self.is_operate = False

    def draw(self, screen: Surface):
        self._draw(
            screen,
            scene.SW - 50,
            scene.SH / 3,
            25,
            scene.SH - scene.SH / 3 - 25
        )
        msg = "  "
        for lenmsg in self.lenmsgs:
            msg+=lenmsg+"  "
        self._draw_str(screen, msg)
        self.command_select(screen,selected=self.selected)

    
    def event(self):
        keys=pygame.key.get_pressed()
        if keys[K_RIGHT] and self.selected<len(self.lenmsgs)-1:
            self.selected+=1
        elif keys[K_LEFT] and self.selected>0:
            self.selected-=1
        return self.is_operate