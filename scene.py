import json
import pygame
from pygame.surface import Surface
from pygame.locals import *
from command import Command
from player import Player
import sys
import mapimgdata
from battle_window import BattleStatusWindow
from layer import Layer
from items.itemdata import items
from context import Context
import command_window
import random
import os
import config
from message import Message
from rain import *
import bgm

rain = []

# 画面サイズ WIDTH
SW = 1280 if len(sys.argv) == 1 else int(sys.argv[1])
# 画面サイズ HEIGHT
SH = 720 if len(sys.argv) == 1 else int(sys.argv[2])
SCR_RECT = Rect(0, 0, SW, SH)  # 画面サイズ

class Scene:
    layer: Layer = None
    name: str = ""
    conf: dict = {}
    events: dict = {}
    is_battle = False
    is_inited = False
    main_menu_win = None
    player_statuses_win = []
    currentplayer = 0

    def __init__(self, layer: Layer, name: str, conf: dict = {}, events: dict = {}) -> None:
        self.layer = layer
        self.name = name
        self.conf = conf
        self.events = events
    
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
                if event.key == K_n:
                    bgm.bgmplay("村")

        if not self.is_inited:
            self.is_inited = True
            for ended_e in scenes.ended_event:
                if  (
                    ended_e["name"] == "chest" and
                    ended_e["map_name"] == self.name
                ):
                    map = None
                    if ended_e["map_layer"] == "map_main":
                       map = self.layer.map 
                    elif ended_e["map_layer"] == "map_everything":
                       map = self.layer.everything
                    elif ended_e["map_layer"] == "map_npcs":
                       map = self.layer.npcs
                    map.map[ended_e["pos"][1]][ended_e["pos"][0]] = 201


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
                            "players": [player.to_dict() for player in players],
                            "ended_event": scenes.ended_event
                        }
                        with open("save_data.json", mode="wt", encoding="utf-8") as f:
                            json.dump(save_data, f, ensure_ascii=False, indent=2)
                        msg = Message("セーブが完了しました",False)
                        msg.draw_until_press_key(screen)
                    elif data["index"] == 6: # 閉じる
                        self.main_menu_win = None
                    elif data["index"] == 7: # マップ一覧 遷移
                        self.main_menu_win.set_commands(Command.NONE, "map_select", [map["name"] for map in config.DEBUG_MAPS])
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
                    for (idx, map) in enumerate(config.MAPS):
                        if map == config.DEBUG_MAPS[data["index"]]["name"]:
                            scenes.current_scene = idx
                    player.x = config.DEBUG_MAPS[data["index"]]["to"][0]
                    player.y = config.DEBUG_MAPS[data["index"]]["to"][1]
                    scenes.scenes[data["index"]].layer.set_pos(
                        (SW - (config.DEBUG_MAPS[data["index"]]["to"][0] * 2)) / 2,
                        (SH - (config.DEBUG_MAPS[data["index"]]["to"][1] * 2)) / 2
                    )
                    self.main_menu_win = None
                    return
            return
        player.event(self.layer, self.conf, scenes, players, screen)

    def draw(self, scenes, players: list, player: Player, screen: Surface):
        pygame.Surface.fill(screen, (0, 0, 0))
        self.layer.draw(screen)
        player.draw(self.layer.map, screen)
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
        if len(rain) < config.RAIN_LEN:
            rain.append(Rain(screen))
            
        # drawRain(rain)

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
    ended_event = []
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
                self.ended_event = json_data["ended_event"]
                x = json_data["pos"]["x"]
                y = json_data["pos"]["y"]
                player_infos = json_data["players"][0]
                player = Player(
                    mapimgdata.load_img("imgs/character/sensi_f.png", -1),
                    *[player_info for player_info in player_infos],
                    x,
                    y
                )
                players = [
                    player,
                    *[Player(
                        mapimgdata.load_img("imgs/character/sensi_f.png", -1),
                        *[p for p in json_data["players"][idx]]) for idx in range(1, len(json_data["players"]))
                    ]
                ]
        else:
            player = Player(mapimgdata.load_img("imgs/character/sensi_f.png", -1), "戦士", 50, 20, 13, 5, 4, 3, 10, 8, 0 ,0, 0, [0], [0 for _ in range(7)], 50, 20, 260, 416) 
            players: list = [
                player,
                Player(mapimgdata.load_img("imgs/character/mahoutsukai_f.png", -1), "魔法使い", 35, 30, 5, 15, 5, 15, 10, 8, 0, 0, 0, [0], [0 for _ in range(7)], 35, 30),
                Player(mapimgdata.load_img("imgs/character/souryo_f.png", -1), "僧侶", 50, 25, 9, 9, 13, 13, 10, 8, 0, 0, 0, [0], [0 for _ in range(7)], 50, 25),
                Player(mapimgdata.load_img("imgs/character/butouka_f.png", -1), "武闘家", 45, 2, 16, 2, 7, 6, 16, 8, 0, 0, 0, [0], [0 for _ in range(7)], 45, 2),
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