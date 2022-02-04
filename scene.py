import pygame
from pygame.surface import Surface
from pygame.locals import *
from command import Command
from player import Player
from map import Map
import sys
import mapimgdata
from message import Message
from monster import Monster
from battle_scene import BattleScene
from layer import Layer
from items.itemdata import items
from items.item import Item
from context import Context
import command_window
import random

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
                    message = Message("HELLO WORLD 日本語対応", True)
                    scenes._messages.append(message)
                if event.key == K_n:
                    message = command_window.CommandWindow(Command.YES_OR_NO)
                    scenes._messages.append(message)
                if event.key == K_b:
                    monsters_num=random.randint(self.conf["monster_info"]["min"],self.conf["monster_info"]["max"])
                    monsters=[]
                    for _ in range(monsters_num):
                        monster_num=random.randint(0,len(self.conf["monster_info"]["kinds"])-1)
                        monsters.append(Monster(self.conf["monster_info"]["kinds"][monster_num]))
                    scene = BattleScene(players, monsters, scenes.current_scene, scenes, screen)
                    scenes.scenes.append(scene)
                    scenes.current_scene = len(scenes.scenes) - 1
                    return
                if event.key == K_i:
                    context = Context(players)
                    for item in items:
                        if item.id == 0:
                            item.callback(context)
                            message = Message(f"{item.name}を使用した", True)
                            scenes._messages.append(message)

        player.proc(scenes.scenes[scenes.current_scene].layer.map, scenes.scenes[scenes.current_scene], scenes)
        is_operate = True
        for msg in scenes._messages:
            msg.draw(screen)
            (is_operate, is_close, data) = msg.event()
            if not is_operate:
                is_operate = False
            if is_close:
                scenes._messages.remove(msg)
                if "msg" in data:
                    if data["msg"] == "はい":
                        print("はいを選んでくれてありがとう!")
        clock.tick(scenes.FPS)
        pygame.display.flip()
        if not is_operate:
            return
        player.event(scenes.scenes[scenes.current_scene].layer)

    def draw(self, scenes, player: Player, screen: Surface):
        pygame.Surface.fill(screen, (0, 0, 0))
        scenes.scenes[scenes.current_scene].layer.draw(screen)
        player.draw(scenes.scenes[scenes.current_scene].layer.map, screen)

class Scenes:
    scenes: list = []
    current_scene = 0
    _win_title: str = ""
    titleicon=""
    _messages: list = []
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
        player = Player(mapimgdata.load_img("imgs/man.png", -1), "戦士", 1000, 50, 10, 10, 10, 10, 10, 0, 0 ,0, 0, [0], [0 for _ in range(7)], 1000, 50, 32, 32)
        players: list = [
            player,
            Player(mapimgdata.load_img("imgs/man.png", -1), "魔法使い", 500, 3, 10, 10, 10, 10, 10, 8, 0, 0, 0, [0], [0 for _ in range(7)], 500, 3),
            Player(mapimgdata.load_img("imgs/man.png", -1), "僧侶", 500, 3, 10, 10, 10, 10, 10, 0, 15, 0, 0, [0], [0 for _ in range(7)], 500, 3),
            Player(mapimgdata.load_img("imgs/man.png", -1), "武闘家", 500, 3, 10, 10, 10, 10, 10, 20, 0, 0, 0, [0], [0 for _ in range(7)], 500, 3),
        ]
        mapimgdata.loaded_imgs()
        clock = pygame.time.Clock()

        while True:
            if self.scenes[self.current_scene].is_battle:
                self.scenes[self.current_scene].draw(self, screen)
                self.scenes[self.current_scene].event(self, clock)
            else:
                self.scenes[self.current_scene].draw(self, player, screen)
                self.scenes[self.current_scene].event(self, players, player, screen, clock)