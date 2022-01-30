from pygame import Surface
from map import Map

class Layer:
    map: Map = None
    everything: Map = None
    npcs: Map = None

    def __init__(self, map: Map, everything: Map, npcs: Map) -> None:
        self.map = map
        self.everything = everything
        self.npcs = npcs

    def draw(self, screen: Surface):
        if self.map != None: self.map.draw(screen) 
        if self.everything != None: self.everything.draw(screen)
        if self.npcs != None: self.npcs.draw(screen)
    
    def set_pos(self, x: int, y: int):
        if self.map != None:
            self.map.x = x
            self.map.y = y
        if self.everything != None:
            self.everything.x = x
            self.everything.y = y
        if self.npcs != None:
            self.npcs.x = x
            self.npcs.y = y

    def set_x(self, x: int):
        if self.map != None: self.map.x = x
        if self.everything != None: self.everything.x = x
        if self.npcs != None: self.npcs.x = x

    def set_y(self, y: int):
        if self.map != None: self.map.y = y
        if self.everything != None: self.everything.y = y
        if self.npcs != None: self.npcs.y = y