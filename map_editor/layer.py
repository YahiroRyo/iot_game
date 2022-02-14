import pygame
import config
from map import Map
from context import Context
from event import KeyEvent
from block_data import BLOCKS, get_block_index_from_id
import json

class Layer(KeyEvent):
    # マップレイヤー
    map: Map = None
    everything: Map = None
    npcs: Map = None

    # マップを隠すフラグ
    hidden_map = False
    hidden_everything = False
    hidden_npcs = False

    is_put = False
    is_scroll = False
    x = 0
    y = 0
    prev_x = 0
    prev_y = 0
    current_map = 0

    def __init__(self, context: Context):
        super().__init__(context)
        context.set("BLOCKS", BLOCKS)
        map_keys = [
            "map_main",
            "map_everything",
            "map_npcs",
        ]
        if config.MAP_IS_LOAD:
            with open(f"../maps/{config.MAP_NAME}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                config.MAP_HEIGHT = len(data["map_main"])
                config.MAP_WIDTH = len(data["map_main"][0])
                config.MAP_CONF = data["conf"]
                for (idx, key) in enumerate(map_keys):
                    blocks = data[key]
                    # マップエディタとの互換性がなかった場合
                    # ※ map_mainのkey必須
                    if len(blocks) == 0:
                        for _ in range(config.MAP_WIDTH):
                            blocks_w = []
                            for _ in range(config.MAP_HEIGHT):
                                blocks_w.append(-1)
                            blocks.append(blocks_w)
                    else:
                        for (idx_y, block_h) in enumerate(blocks):
                            for (idx_x, block_idx) in enumerate(block_h):
                                blocks[idx_y][idx_x] = get_block_index_from_id(block_idx)
                    if idx == 0: self.map = Map(context, blocks)
                    if idx == 1: self.everything = Map(context, blocks)
                    if idx == 2: self.npcs = Map(context, blocks)
        else:
            bg = -1
            for (idx, block) in enumerate(BLOCKS):
                if block.id == config.MAP_BG_ID:
                    bg = idx
            for (idx, _) in enumerate(map_keys):
                blocks = []
                for _ in range(config.MAP_WIDTH):
                    blocks_w = []
                    for _ in range(config.MAP_HEIGHT):
                        blocks_w.append(bg)
                    blocks.append(blocks_w)
                if idx == 0: self.map = Map(context, blocks)
                if idx == 1: self.everything = Map(context, blocks)
                if idx == 2: self.npcs = Map(context, blocks)
                bg = -1

    def draw(self):
        if self.map != None and not self.hidden_map: self.map.draw() 
        if self.everything != None and not self.hidden_everything: self.everything.draw()
        if self.npcs != None and not self.hidden_npcs: self.npcs.draw()
    
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

    def mouse_down_right(self, context: Context):
        (x, y) = pygame.mouse.get_pos()
        self.is_scroll = True
        self.prev_x = self.x - x
        self.prev_y = self.y - y

    def mouse_up_right(self, context: Context):
        self.is_scroll = False

    def mouse_down_left(self, context: Context):
        (x, _) = pygame.mouse.get_pos()
        if context.current_block != -1 and x >= context.get("SW") / 3:
            self.is_put = True

    def mouse_up_left(self, context: Context):
        self.is_put = False
    
    def after_event(self, context: Context):
        (x, y) = pygame.mouse.get_pos()
        if self.is_put:
            try:
                if self.current_map == 0:
                    self.map.blocks[int((y - self.y) / config.MAP_MSIZE )][int((x - self.x - self.context.get("SW") / 3) / config.MAP_MSIZE)] = context.current_block
                if self.current_map == 1:
                    self.everything.blocks[int((y - self.y) / config.MAP_MSIZE )][int((x - self.x - self.context.get("SW") / 3) / config.MAP_MSIZE)] = context.current_block
                if self.current_map == 2:
                    self.npcs.blocks[int((y - self.y) / config.MAP_MSIZE )][int((x - self.x - self.context.get("SW") / 3) / config.MAP_MSIZE)] = context.current_block
            except:
                pass
            
        if self.is_scroll:
            self.x = self.prev_x + x
            self.y = self.prev_y + y
            self.set_pos(self.x, self.y)