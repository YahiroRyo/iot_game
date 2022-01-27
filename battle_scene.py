from commandmsg import CommandWindow
from pygame.surface import Surface
from message import Message
from pygame.locals import *
from battle_window import BattleStatusWindow
import pygame
import scene
import sys
import mapimgdata
import monster

class BattleScene:
    is_battle = True
    current_scene = 0
    players: list = []
    monsters: list = []
    monster_imgs: list = []
    message: Message
    battle_status_windows: list = []


    def __init__(self, players: list, monsters: list, current_scene: int) -> None:
        self.current_scene = current_scene
        self.players = players
        self.monsters = monsters
        self.message = Message("", True)
        self.command_win = CommandWindow(2, scene.SW - 25, 48, 12.5, scene.SH - scene.SH / 3 - 36.5)
        self.battle_status_windows = [BattleStatusWindow() for _ in players]
        self.monster_imgs = [mapimgdata.load_img(f"imgs/monsters/{monster.img}", -1) for monster in monsters]

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
                    self.command_win.set_commands("to_monster", [monster.name for monster in self.monsters])
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
                if cmd["index"]==0:
                    self.attack(self.players[0], self.monsters[0])
                elif cmd["index"]==1:
                     self.attack(self.players[1], self.monsters[1])
                elif cmd["index"]==2:
                     self.attack(self.players[2], self.monsters[2])
                elif cmd["index"]==3:
                     self.attack(self.players[3], self.monsters[3])
                elif cmd["index"]==4:
                     self.attack(self.players[4], self.monsters[4])
                elif cmd["index"]==5:
                     self.attack(self.players[5], self.monsters[5])
                elif cmd["index"]==6:
                     self.attack(self.players[6], self.monsters[6])
                elif cmd["index"]==7:
                     self.attack(self.players[7], self.monsters[7])



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
            screen.blit(
                monster_img,
                (x + (idx * 140), scene.SH / 3)
            )

    def attack(self, _from, _to):
        dmg=_from.power    #monster.Monster.random(_from.power)
        _to.hp -= dmg*1000
        if _to.hp<0:
            _to.hp=0
        self.hp_check()
        return


    def hp_check(self):
        for index, player in enumerate(self.players):
            if player.hp<=0:
                self.dead(index ,player)
        for index, monster in enumerate(self.monsters):
            if monster.hp<=0:
                self.dead(index, monster)
        return


    def dead(self, index, obj):
        self.message.msg=obj.name+"は死んでしまった。嗚呼、死んでしまうとは情けない…"#死亡メッセージ
        if obj.__class__ == "Player":
            print("player")
        else:
            self.remove_monster(index)
            print("monster")
        return