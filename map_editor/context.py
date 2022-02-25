import config
from pygame import Surface

class Context:
    _storage: dict = {}
    screen: Surface = None
    layer = None
    current_block = -1
    current_mode = 0

    current_select_block = [-1, -1]
    events = {
        "map_main": [],
        "map_everything": [],
        "map_npcs": [],
    }

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
    
    def get_current_map(self, current_map: int):
        key = ""
        if current_map == 0: key = "map_main"
        if current_map == 1: key = "map_everything"
        if current_map == 2: key = "map_npcs"
        return key

    def get_current_select_block(self):
        x = self.current_select_block[1]
        y = self.current_select_block[0]
        return [x, y]