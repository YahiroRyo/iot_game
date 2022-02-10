import config
import pygame_gui
from pygame import Surface

class Context:
    _storage: dict = {}
    screen: Surface = None
    manager: pygame_gui.UIManager = None
    map = None
    current_block = -1

    def __init__(self):
        self.set("SW", config.SW)
        self.set("SH", config.SH)
        self.set("ML", config.ML)
        self.set("MM", config.MM)
        self.set("MR", config.MR)
        self.set("FPS", config.FPS)
        self.set("MAP_WIDTH", config.MAP_WIDTH)
        self.set("MAP_HEIGHT", config.MAP_HEIGHT)
        self.set("MAP_NAME", config.MAP_NAME)
        
    def set(self, key: str, value):
        self._storage[key] = value
        
    def get(self, key: str):
        return self._storage[key]