import time
from command import Command
from command_window import CommandWindow
from pygame.surface import Surface
from message import Message
from pygame.locals import *
from battle_window import BattleStatusWindow
import color
import pygame
import scene
import sys
import mapimgdata

class BattleScene:
    is_battle = True
    current_scene = 0
    players: list = []
    monsters: list = []
    monster_imgs: list = []
    message: Message
    battle_status_windows: list = []
    font = None
    get_exp=0
    scenes=None
    screen=None

    def __init__(self, players: list, monsters: list, current_scene: int, scenes, screen: Surface) -> None:
        self.current_scene = current_scene
        self.players = players
        self.monsters = monsters
        self.message = Message("", True)
        self.command_win = CommandWindow(Command.BATTLE_SELECT, scene.SW - 25, 48, 12.5, scene.SH / 6)
        self.battle_status_windows = [BattleStatusWindow() for _ in players]
        self.monster_imgs = [mapimgdata.load_img(f"imgs/monsters/{monster.img}", -1) for monster in monsters]
        self.font = pygame.font.Font("fonts/PixelMplus10-Regular.ttf", 24)
        self.scenes=scenes
        self.screen = screen

    def remove_monster(self, remove_index):
        self.monsters.remove(self.monsters[remove_index])
        self.monster_imgs.remove(self.monster_imgs[remove_index])

    def back_to_current_scene(self, scenes):
        scenes.scenes.remove(self)
        scenes.current_scene = self.current_scene

    def event(self, scenes, clock: pygame.time.Clock):
        for event in pygame.event.get():
            # 終了用のイベント処理
            if event.type == QUIT:          # 閉じるボタンが押されたとき
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:       # キーを押したとき
                if event.key == K_ESCAPE:   # Escキーが押されたとき
                    pygame.quit()
                    sys.exit()
                #if event.key == K_RETURN:
                #    self.back_to_current_scene()
                #    return

        self.message.event()
        (is_operate, is_close, cmd) = self.command_win.event()
        if "index" in cmd:
            if cmd["unique"] == "battle_select":
                if cmd["index"]==0:
                    self.command_win.set_commands(Command.NONE, "to_monster", [monster.name for monster in self.monsters])
                    #self.attack(self.players[0], self.monsters[0])
                    pass
                elif cmd["index"]==1:
                    pass
                elif cmd["index"]==2:
                    pass
                elif cmd["index"]==3:
                    pass
                elif cmd["index"]==4:
                    pass
                elif cmd["index"]==5:
                    self.back_to_current_scene(scenes)
                    return
            elif cmd["unique"] == "to_monster":
                self.attack(self.players[0], self.monsters[cmd["index"]])
                self.command_win.set_commands(Command.BATTLE_SELECT)

        clock.tick(scenes.FPS)
        pygame.display.flip()
        
    def draw(self, scenes, screen: Surface):
        pygame.Surface.fill(screen, (0, 0, 0))
        self.message.draw(screen)
        self.command_win.draw(screen)
        for idx, battle_status_window in enumerate(self.battle_status_windows):
            battle_status_window.draw(screen, idx * scene.SW / 4, self.players[idx].name, self.players[idx].hp, self.players[idx].mp)
        x = scene.SW / 2 - (len(self.monsters) * 140) / 2
        for idx, monster_img in enumerate(self.monster_imgs):
            text = self.font.render(self.monsters[idx].name, True, color.WHITE)
            screen.blit(
                monster_img,
                (x + idx * 140, scene.SH / 3)
            )
            screen.blit(
                text,
                (x + idx * 140, scene.SH / 3 + 140)
            )

    def attack(self, _from, _to):
        dmg=_from.power    #monster.Monster.random(_from.power)
        _to.hp -= dmg
        if _to.hp<0:
            _to.hp=0
        self.message.msg=_from.name+"は"+_to.name+"に"+str(dmg)+"ダメージ与えた"
        self.hp_check()
        return


    def hp_check(self):
        for index, player in enumerate(self.players):
            if player.hp<=0:
                self.dead(index ,player)
        for index, monster in enumerate(self.monsters):
            if monster.hp<=0:
                self.get_exp += monster.exp
                self.dead(index, monster)
        return


    def dead(self, index, obj):
        self.message.msg=self.message.msg+"\n"+obj.name+"は死んでしまった。嗚呼、死んでしまうとは情けない…"#死亡メッセージ
        if obj.__class__ == "Player":
            print("player")
        else:
            self.remove_monster(index)
            self.hp_check()
        if len(self.monsters) == 0:
            print(f"{self.get_exp}ポイントの経験値を手に入れた")
            self.message.msg = str(self.get_exp)+"ポイントの経験値とお金を手に入れた"
            self.message.draw_until_press_key(self.screen)
            self.players[0].money+=self.get_exp
            for player in self.players:
                player.exp+=self.get_exp
            print(f"{self.players[0].money},{self.players[0].exp}")
            self.back_to_current_scene(self.scenes)
        return