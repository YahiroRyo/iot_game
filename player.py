from enum import Enum
import pygame
from pygame.surface import Surface
from pygame.locals import *
from layer import Layer
from monster import Params
from map import Map
from mapimgdata import load_img
import scene as iscene
import math

WALLS = [0, 1, 2]
SHIP_WALLS = [i for i in range(2, 111)]

class PLAYER_MODE(Enum):
    WALK = 0
    SHIP = 1

# プレイヤー
class Player(Params):
    # バトル関係
    items: list = []
    exp: int = 0
    money=0
    img = None
    x = 32
    y = 32
    size = 30
    speed = 1

    mode = PLAYER_MODE.WALK
    
    def __init__(self, *args):
        self.img = args[0]
        self.name = args[1]
        self.hp = args[2]
        self.mp = args[3]
        self.power = args[4]
        self.m_power = args[5]
        self.defense = args[6]
        self.m_defense = args[7]
        self.agility = args[8]
        self.luck = args[9]
        self.lv = args[10]
        self.exp = args[11]
        self.money = args[12]
        self.items = args[13]
        self.flgs = args[14]
        self.maxhp= args[15]
        self.maxmp = args[16]
        if len(args) >=18:
            self.x = args[17]
            self.y = args[18]
        
    def to_dict(self):
        return [
            self.name,
            self.hp,
            self.mp,
            self.power,
            self.m_power,
            self.defense,
            self.m_defense,
            self.agility,
            self.luck,
            self.lv,
            self.exp,
            self.money,
            self.items,
            self.flgs,
            self.maxhp,
            self.maxmp,
        ]

    # プレイヤーの描画
    def draw(self, map: Map, screen: Surface) -> None:
        screen.blit(self.img, (self.x + map.x, self.y + map.y))

    def get_positions(self, key: int):
        x = 0
        y = 0
        tmp_x = 0
        tmp_y = 0
        
        if key == K_UP:
            y -= self.speed
            tmp_x = self.size
        if key == K_DOWN:
            y += self.size + self.speed
            tmp_x = self.size
        if key == K_LEFT:
            x -= self.speed
            tmp_y = self.size
        if key == K_RIGHT:
            x += self.size + self.speed
            tmp_y = self.size
        return (x, y, tmp_x, tmp_y)

    def get_keys(self):
        ret: list = []
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
           ret.append(K_UP) 
        if keys[K_DOWN]:
           ret.append(K_DOWN) 
        if keys[K_LEFT]:
           ret.append(K_LEFT) 
        if keys[K_RIGHT]:
           ret.append(K_RIGHT) 
        return ret
    
    def key_is_wall(self, key: int, map: Map):
        (x, y, tmp_x, tmp_y) = self.get_positions(key)
        if self.mode == PLAYER_MODE.WALK:
            return self.get_block(map, self.x + x, self.y + y) in WALLS or self.get_block(map, self.x + tmp_x + x, self.y + tmp_y + y) in WALLS
        else:
            return self.get_block(map, self.x + x, self.y + y) in SHIP_WALLS or self.get_block(map, self.x + tmp_x + x, self.y + tmp_y + y) in SHIP_WALLS

    def event(self, layer: Layer):
        keys = pygame.key.get_pressed()
        img_mode = ""
        if self.mode == PLAYER_MODE.WALK:
            img_mode = "sensi"
        if self.mode == PLAYER_MODE.SHIP:
            img_mode = "ship"
        if keys[K_UP]:
            if not self.key_is_wall(K_UP, layer.map) and self.y > 0:
                self.img = load_img(f"imgs/character/{img_mode}_b.png", -1)
                self.y -= self.speed
                layer.set_y(layer.map.y + self.speed)
        if keys[K_DOWN]:
            if not self.key_is_wall(K_DOWN, layer.map) and self.y < layer.map.row * layer.map.msize - self.size:
                self.img = load_img(f"imgs/character/{img_mode}_f.png", -1)
                self.y += self.speed
                layer.set_y(layer.map.y - self.speed)
        if keys[K_LEFT]:
            if not self.key_is_wall(K_LEFT, layer.map) and self.x > 0:
                self.img = load_img(f"imgs/character/{img_mode}_l.png", -1)
                self.x -= self.speed
                layer.set_x(layer.map.x + self.speed)
        if keys[K_RIGHT]:
            if not self.key_is_wall(K_RIGHT, layer.map) and self.x < layer.map.col * layer.map.msize - self.size:
                self.img = load_img(f"imgs/character/{img_mode}_r.png", -1)
                self.x += self.speed
                layer.set_x(layer.map.x - self.speed)

    def get_block(self, map: Map, x: int = -1, y: int = -1):
        tmp_x = self.x if x == -1 else x
        tmp_y = self.y if y == -1 else y
        block = 0
        # マップ外を見ようとするとエラーがでる index out of range
        try:
            block = map.map[math.floor(tmp_y / map.msize)][math.floor(tmp_x / map.msize)]
        except:
            pass
        return block

    def proc(self, layer: Layer, scene, scenes):
        keys = self.get_keys()
        for key in keys:
            r = self.get_block(layer.map, self.x + 30, self.y)
            r_b = self.get_block(layer.map, self.x + 30, self.y + 30)
            l = self.get_block(layer.map, self.x, self.y)
            l_b = self.get_block(layer.map, self.x, self.y + 30)
            for events in scene.events.values():
                if len(events) != 0:
                    for event in events:
                        if "pos" in event and event["pos"] == [int(self.x / layer.map.msize), int(self.y / layer.map.msize)]:
                            # 乗船
                            if event["name"] == "to_sea":
                                self.mode = PLAYER_MODE.SHIP
                                return  
                        # 遷移システム作成
                        if "from_pos" in event and (
                            event["from_pos"] == [int((self.x + 30) / layer.map.msize), int((self.y) / layer.map.msize)] or
                            event["from_pos"] == [int((self.x + 30) / layer.map.msize), int((self.y + 30) / layer.map.msize)] or
                            event["from_pos"] == [int((self.x) / layer.map.msize), int((self.y) / layer.map.msize)] or
                            event["from_pos"] == [int((self.x) / layer.map.msize), int((self.y + 30) / layer.map.msize)] 
                        ):
                            if event["name"] == "to_other_map":
                                for i, v in enumerate(scenes.scenes):
                                    if v.name == event["other_map_name"]:
                                        scenes.current_scene = i
                                        self.x = event["pos"][0]
                                        self.y = event["pos"][1]
                                        scenes.scenes[i].layer.set_pos(
                                            (iscene.SW - (event["pos"][0] * 2)) / 2,
                                            (iscene.SH - (event["pos"][1] * 2)) / 2
                                        )
                                        return
                                
            for k in scene.conf:
                # stringをintに変更できないというエラーが発生する
                try:
                    if r == int(k) or r_b == int(k) or l == int(k) or l_b == int(k):
                        for i, v in enumerate(scenes.scenes):
                            if v.name == scene.conf[k][0]:
                                scenes.current_scene = i
                                self.x = scene.conf[k][1]
                                self.y = scene.conf[k][2]
                                scenes.scenes[i].layer.set_pos(
                                    (iscene.SW - (scene.conf[k][1] * 2)) / 2,
                                    (iscene.SH - (scene.conf[k][2] * 2)) / 2
                                )
                                return
                except:
                    pass