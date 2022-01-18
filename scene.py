import pygame
from pygame.event import Event
from pygame.surface import Surface
from pygame.locals import *
from player import Player
from map import Map
import sys
import mapimgdata
from message import Message

# 画面サイズ WIDTH
SW = 640 if len(sys.argv) == 1 else int(sys.argv[1])
# 画面サイズ HEIGHT
SH = 480 if len(sys.argv) == 1 else int(sys.argv[2])
SCR_RECT = Rect(0, 0, SW, SH)  # 画面サイズ

class Scene:
    map: Map
    name: str = ""
    conf: dict = {}

    def __init__(self, map: Map, name: str, conf: dict = {}) -> None:
        self.map = map
        self.name = name
        self.conf = conf

class Scenes:
    scenes: list = []
    current_scene = 0
    _win_title: str = ""
    _messages: list = []

    def __init__(self, window_title: str = "GAME") -> None:
        self._win_title = window_title

    def set_scene(self, scene: Scene):
        self.scenes.append(scene)

    def start(self):
        pygame.init()
        pygame.display.set_caption(self._win_title)
        screen = pygame.display.set_mode(SCR_RECT.size)
        player = Player(mapimgdata.load_img("imgs/man.png", -1))
        mapimgdata.loaded_imgs()

        while True:
            pygame.Surface.fill(screen, (0, 0, 0))
            player.event(self.scenes[self.current_scene].map)
            player.proc(self.scenes[self.current_scene].map, self.scenes[self.current_scene], self)
            self.scenes[self.current_scene].map.draw(screen)
            player.draw(self.scenes[self.current_scene].map, screen)
            for msg in self._messages:
                msg.draw(screen)
                msg.event()
            pygame.display.update()

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
                        message = Message("HELLO WORLD")
                        self._messages.append(message)