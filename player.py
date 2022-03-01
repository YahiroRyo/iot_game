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
from items.itemdata import items
import random
from monster import Monster
from monsterdata import monster_data
from battle_scene import BattleScene

WALLS = [0, 1, 2, 14, 200, 201]
SHIP_WALLS = [i for i in range(2, 106)]

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
    allow = K_UP

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

    def event(self, layer: Layer, conf: dict, scenes, players, screen):
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
                self.allow = K_UP
                layer.set_y(layer.map.y + self.speed)
                self.encounter(conf, scenes , players, screen)#エンカウント部分をコメントアウト中
        if keys[K_DOWN]:
            if not self.key_is_wall(K_DOWN, layer.map) and self.y < layer.map.row * layer.map.msize - self.size:
                self.img = load_img(f"imgs/character/{img_mode}_f.png", -1)
                self.y += self.speed
                self.allow = K_DOWN
                layer.set_y(layer.map.y - self.speed)
                #self.encounter(conf, scenes , players, screen)        
        if keys[K_LEFT]:
            if not self.key_is_wall(K_LEFT, layer.map) and self.x > 0:
                self.img = load_img(f"imgs/character/{img_mode}_l.png", -1)
                self.x -= self.speed
                self.allow = K_LEFT
                layer.set_x(layer.map.x + self.speed)
                #self.encounter(conf, scenes , players, screen)        
        if keys[K_RIGHT]:
            if not self.key_is_wall(K_RIGHT, layer.map) and self.x < layer.map.col * layer.map.msize - self.size:
                self.img = load_img(f"imgs/character/{img_mode}_r.png", -1)
                self.x += self.speed
                self.allow = K_RIGHT
                layer.set_x(layer.map.x - self.speed)
                #self.encounter(conf, scenes , players, screen)        

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
        r = self.get_block(layer.map, self.x + 30, self.y)
        r_b = self.get_block(layer.map, self.x + 30, self.y + 30)
        l = self.get_block(layer.map, self.x, self.y)
        l_b = self.get_block(layer.map, self.x, self.y + 30)
        for key, events in scene.events.items():
            if len(events) != 0:
                for event in events:
                    if "pos" in event and event["pos"] == [int(self.x / layer.map.msize), int(self.y / layer.map.msize)]:
                        # 乗船
                        if event["name"] == "to_sea":
                            self.mode = PLAYER_MODE.SHIP
                            return  
                        if event["name"] == "to_land":
                            self.mode = PLAYER_MODE.WALK
                            return  
                    if "pos" in event and event["name"] == "chest":
                        is_exist = False
                        if self.allow == K_RIGHT:
                            is_exist = (
                                event["pos"] == [int((self.x + 64) / layer.map.msize), int((self.y + 15) / layer.map.msize)] or 
                                event["pos"] == [int((self.x + 32) / layer.map.msize), int((self.y + 15) / layer.map.msize)] 
                            )
                        elif self.allow == K_LEFT:
                            is_exist = event["pos"] == [int((self.x - 32) / layer.map.msize), int((self.y + 15) / layer.map.msize)]
                        elif self.allow == K_DOWN:
                            is_exist = (
                                event["pos"] == [int((self.x + 15) / layer.map.msize), int((self.y + 64) / layer.map.msize)] or 
                                event["pos"] == [int((self.x + 15) / layer.map.msize), int((self.y + 32) / layer.map.msize)]
                            )
                        elif self.allow == K_UP:
                            is_exist =  event["pos"] == [int((self.x + 15) / layer.map.msize), int((self.y - 32) / layer.map.msize)]
                            
                        if is_exist and (
                            len(scenes.ended_event) == 0 or True in [
                                    ended_e["name"] != event["name"] and
                                    ended_e["pos"] != event["pos"] and
                                    ended_e["name"] != scenes.scenes[scenes.current_scene].name and
                                    ended_e["map_layer"] != key
                                    for ended_e in scenes.ended_event
                                ]
                            ):
                            press_keys = pygame.key.get_pressed()
                            if press_keys[K_RETURN]:
                                item_idx = 0
                                for (idx, item) in enumerate(items):
                                    if item.id == event["item_id"]:
                                        item_idx = idx
                                        break
                                self.items.append(item_idx)
                                scenes.ended_event.append({
                                    "map_layer": key,
                                    "map_name": scenes.scenes[scenes.current_scene].name,
                                    "name": event["name"],
                                    "pos": event["pos"],
                                })
                                map = None
                                if key == "map_main":
                                   map = scenes.scenes[scenes.current_scene].layer.map 
                                elif key == "map_everything":
                                   map = scenes.scenes[scenes.current_scene].layer.everything
                                elif key == "map_npcs":
                                   map = scenes.scenes[scenes.current_scene].layer.npcs
                                map.map[event["pos"][1]][event["pos"][0]] = 201
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
    
    def encounter(self, conf: dict, scenes, players, screen):
        enc=random.randint(1,2)
        if enc==1:
            if conf["monster_info"]["min"] != 0 and conf["monster_info"]["max"] != 0:
                monsters_num=random.randint(conf["monster_info"]["min"],conf["monster_info"]["max"])
                monsters=[]
                for _ in range(monsters_num):
                    monster_num=random.randint(0,len(conf["monster_info"]["kinds"])-1)
                    monsters.append(Monster(monster_data[conf["monster_info"]["kinds"][monster_num]]))
                scene = BattleScene(players, monsters, scenes.current_scene, scenes, screen)
                scenes.scenes.append(scene)
                scenes.current_scene = len(scenes.scenes) - 1
                return