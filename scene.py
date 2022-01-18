import pygame
from pygame.event import Event
from pygame.surface import Surface
from pygame.locals import *
from player import Player
from map import Map
import sys

# 画面サイズ WIDTH
SW = 640 if len(sys.argv) == 1 else int(sys.argv[1])
# 画面サイズ HEIGHT
SH = 480 if len(sys.argv) == 1 else int(sys.argv[2])
SCR_RECT = Rect(0, 0, SW, SH)  # 画面サイズ

def load_img(filename, colorkey=None):
    img = pygame.image.load(filename)
    img = img.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey, RLEACCEL)
    return img

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

    def __init__(self, window_title: str = "GAME") -> None:
        self._win_title = window_title

    def set_scene(self, scene: Scene):
        self.scenes.append(scene)

    def start(self):
        pygame.init()
        pygame.display.set_caption(self._win_title)
        screen = pygame.display.set_mode(SCR_RECT.size)
        player = Player(load_img("imgs/man.png", -1))
        Map.imgs[0] = load_img("imgs/grass.png")
        Map.imgs[1] = load_img("imgs/water.png")
        Map.imgs[2] = load_img("imgs/wall.png")
        Map.imgs[3] = load_img("imgs/rock.png")
        Map.imgs[4] = load_img("imgs/black.png")
        Map.imgs[10] = load_img("imgs/warp.png")
        Map.imgs[11] = load_img("imgs/cave.png")

        while True:
            pygame.Surface.fill(screen, (0, 0, 0))
            player.event(self.scenes[self.current_scene].map)
            player.proc(self.scenes[self.current_scene].map, self.scenes[self.current_scene], self)
            self.scenes[self.current_scene].map.draw(screen)
            player.draw(self.scenes[self.current_scene].map, screen)
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
