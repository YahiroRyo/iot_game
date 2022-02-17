import json
import pygame
from pygame.surface import Surface
from pygame.locals import *
from command import Command
from player import Player
import sys
import mapimgdata
from monster import Monster
from battle_window import BattleStatusWindow
from battle_scene import BattleScene
from layer import Layer
from items.itemdata import items
from context import Context
import command_window
import random
import os
import config
from message import Message
from monsterdata import monster_data

# 画面サイズ WIDTH
SW = 1280 if len(sys.argv) == 1 else int(sys.argv[1])
# 画面サイズ HEIGHT
SH = 720 if len(sys.argv) == 1 else int(sys.argv[2])
SCR_RECT = Rect(0, 0, SW, SH)  # 画面サイズ

class Scene:
    map: Layer
    name: str = ""
    conf: dict = {}
    is_battle = False
    main_menu_win = None
    player_statuses_win = []
    currentplayer = 0

    def __init__(self, layer: Layer, name: str, conf: dict = {}) -> None:
        self.layer = layer
        self.name = name
        self.conf = conf
    
    def event(self, scenes, players: list, player: Player, screen: Surface, clock: pygame.time.Clock):
        for event in pygame.event.get():
            # 終了用のイベント処理
            if event.type == QUIT:          # 閉じるボタンが押されたとき
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:       # キーを押したとき
                if event.key == K_ESCAPE:   # Escキーが押されたとき
                    pygame.quit()
                    sys.exit()
                if event.key == K_m:
                    MARGIN = 50
                    self.main_menu_win = command_window.CommandWindow(Command.MAIN_MENU)
                    self.player_statuses_win = [BattleStatusWindow() for _ in players]
                if event.key == K_b:
                    if self.conf["monster_info"]["min"] != 0 and self.conf["monster_info"]["max"] != 0:
                        monsters_num=random.randint(self.conf["monster_info"]["min"],self.conf["monster_info"]["max"])
                        monsters=[]
                        for _ in range(monsters_num):
                            monster_num=random.randint(0,len(self.conf["monster_info"]["kinds"])-1)
                            monsters.append(Monster(monster_data[self.conf["monster_info"]["kinds"][monster_num]]))
                        scene = BattleScene(players, monsters, scenes.current_scene, scenes, screen)
                        scenes.scenes.append(scene)
                        scenes.current_scene = len(scenes.scenes) - 1
                        return

        player.proc(scenes.scenes[scenes.current_scene].layer, scenes.scenes[scenes.current_scene], scenes)
        is_operate = True
        clock.tick(scenes.FPS)
        pygame.display.flip()
        if not is_operate:
            return
        if self.main_menu_win != None:
            (is_operate, is_close, data) = self.main_menu_win.event()
            if "index" in data:
                # メニューの名前によって処理を変えてね
                if data["unique"] == "main_menu":
                    if data["index"] == 0: # ステータス
                        self.main_menu_win.set_commands(Command.NONE, "status", ["戻る"])
                        pass
                    elif data["index"] == 1: # 魔法
                        pass
                    elif data["index"] == 2: # 道具
                        if len(player.items) != 0:
                            self.main_menu_win.set_commands(Command.NONE, "player_items", [items[id].name for id in player.items])
                        else:
                            pass
                        pass
                    elif data["index"] == 3: # 経験値
                        self.main_menu_win.set_commands(Command.NONE, "character_select", [player.name for player in players])
                        pass
                    elif data["index"] == 4: # 設定
                        pass
                    elif data["index"] == 5: # セーブ
                        self.main_menu_win = None
                        save_data = {
                            "map": {
                                "current_scene": scenes.current_scene,
                                "x": self.layer.map.x,
                                "y": self.layer.map.y,
                            },
                            "pos": {
                                "x": player.x,
                                "y": player.y,
                            }, 
                            "players": [player.to_dict() for player in players]
                        }
                        with open("save_data.json", mode="wt", encoding="utf-8") as f:
                            json.dump(save_data, f, ensure_ascii=False, indent=2)
                        msg = Message("セーブが完了しました",False)
                        msg.draw_until_press_key(screen)
                    elif data["index"] == 6: # 閉じる
                        self.main_menu_win = None
                    elif data["index"] == 7: # マップ一覧 遷移
                        self.main_menu_win.set_commands(Command.NONE, "map_select", [map for map in config.MAPS])
                elif data["unique"] == "status":# ステータス
                    self.main_menu_win.set_commands(Command.MAIN_MENU)
                    self.player_statuses_win = [BattleStatusWindow() for _ in players]
                elif data["unique"] == "player_items":# アイテム使用時
                    context = Context(players, None)
                    items[data["index"]].callback(context)
                    player.items.remove(data["index"])
                    self.main_menu_win = None
                elif data["unique" ] == "character_select":
                    self.currentplayer = data["index"]
                    self.player_statuses_win = [BattleStatusWindow()]
                    self.main_menu_win.set_commands(Command.NONE, "status_panel", ["ＨＰ", "ＭＰ", "攻撃力", "防御力", "魔法攻撃力", "魔法防御力", "素早さ", "会心", "閉じる"])
                elif data["unique"] == "status_panel":# ステータス振り分け
                    if data["index"] == 8:
                        self.main_menu_win = None
                    else:
                        self.status_up(players[self.currentplayer], data["index"])
                elif data["unique"] == "map_select":
                    for map in config.DEBUG_MAPS:
                        if config.MAPS[data["index"]] == map["name"]:
                            scenes.current_scene = data["index"]
                            player.x = map["to"][0]
                            player.y = map["to"][1]
                            scenes.scenes[data["index"]].layer.set_pos(
                                (SW - (map["to"][0] * 2)) / 2,
                                (SH - (map["to"][1] * 2)) / 2
                            )
                            for _ in pygame.key.get_pressed():
                                pass
                            self.main_menu_win = None
                            return
            return
        player.event(scenes.scenes[scenes.current_scene].layer)

    def draw(self, scenes, players: list, player: Player, screen: Surface):
        pygame.Surface.fill(screen, (0, 0, 0))
        scenes.scenes[scenes.current_scene].layer.draw(screen)
        player.draw(scenes.scenes[scenes.current_scene].layer.map, screen)
        if self.main_menu_win != None:
            self.main_menu_win.draw(screen)
            if len(self.player_statuses_win) != 0:
                for (idx, player_status_win) in enumerate(self.player_statuses_win):
                    if self.main_menu_win.unique_name == "status":
                        player_status_win.draw_status(screen, players[idx], idx * SW / 4)
                    elif self.main_menu_win.unique_name == "status_panel":
                        player_status_win.draw_status(screen, players[self.currentplayer], self.currentplayer * SW / 4)
                    else:
                        player_status_win.draw(screen, idx * SW / 4, players[idx].name, players[idx].hp, players[idx].mp, players[idx].maxhp, players[idx].maxmp)
    
    def status_up(self, currentplayer, currentstatus):
        if currentplayer.exp >= 10:
            if currentstatus == 0:
                currentplayer.maxhp += 1
            elif currentstatus == 1:
                currentplayer.maxmp += 1
            elif currentstatus == 2:
                currentplayer.power += 1
            elif currentstatus == 3:
                currentplayer.defense += 1
            elif currentstatus == 4:
                currentplayer.m_power += 1
            elif currentstatus == 5:
                currentplayer.m_defense += 1
            elif currentstatus == 6:
                currentplayer.agility += 1
            elif currentstatus == 7:
                currentplayer.luck += 1
            currentplayer.lv += 1
            currentplayer.exp -= 10

class Scenes:
    scenes: list = []
    current_scene = 0
    _win_title: str = ""
    titleicon=""
    FPS = 120

    def __init__(self, window_title: str = "GAME", titleicon:str = None) -> None:
        self._win_title = window_title
        self.titleicon=pygame.image.load(titleicon)
        pygame.display.set_icon(self.titleicon)

    def set_scene(self, scene: Scene):
        self.scenes.append(scene)

    def start(self):
        pygame.init()
        pygame.display.set_caption(self._win_title)
        screen = pygame.display.set_mode(SCR_RECT.size)
        is_exist_file = os.path.isfile("save_data.json")
        player = None
        players = []
        if is_exist_file:
            with open("save_data.json", "r", encoding="utf-8") as f:
                json_data = json.load(f)
                self.current_scene = json_data["map"]["current_scene"]
                self.scenes[self.current_scene].layer.set_pos(json_data["map"]["x"], json_data["map"]["y"])
                x = json_data["pos"]["x"]
                y = json_data["pos"]["y"]
                player_infos = json_data["players"][0]
                player = Player(
                    mapimgdata.load_img("imgs/man.png", -1),
                    *[player_info for player_info in player_infos],
                    x,
                    y
                )
                players = [
                    player,
                    *[Player(
                        mapimgdata.load_img("imgs/man.png", -1),
                        *[p for p in json_data["players"][idx]]) for idx in range(1, len(json_data["players"]))
                    ]
                ]
        else:
            player = Player(mapimgdata.load_img("imgs/character/sensi_f.png", -1), "戦士", 1000, 50, 10, 10, 10, 10, 10, 0, 1000 ,1000, 0, [0], [0 for _ in range(7)], 1000, 50, 260, 416) 
            players: list = [
                player,
                Player(mapimgdata.load_img("imgs/character/mahoutsukai_f.png", -1), "魔法使い", 500, 3, 10, 10, 10, 10, 10, 8, 0, 0, 0, [0], [0 for _ in range(7)], 500, 3),
                Player(mapimgdata.load_img("imgs/character/souryo_f.png", -1), "僧侶", 500, 3, 10, 10, 10, 10, 10, 0, 15, 0, 0, [0], [0 for _ in range(7)], 500, 3),
                Player(mapimgdata.load_img("imgs/character/butouka_f.png", -1), "武闘家", 500, 3, 10, 10, 10, 10, 10, 20, 0, 0, 0, [0], [0 for _ in range(7)], 500, 3),
            ]
            self.scenes[self.current_scene].layer.set_pos(
                                (SW - (260 * 2)) / 2,
                                (SH - (416 * 2)) / 2
                            )
        mapimgdata.loaded_imgs()
        clock = pygame.time.Clock()

        while True:
            if self.scenes[self.current_scene].is_battle:
                self.scenes[self.current_scene].draw(self, screen)
                self.scenes[self.current_scene].event(self, clock)
            else:
                self.scenes[self.current_scene].draw(self, players, player, screen)
                self.scenes[self.current_scene].event(self, players, player, screen, clock)