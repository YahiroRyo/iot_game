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
import math
import random

class BattleScene:
    is_battle = True
    current_scene = 0
    players: list = []
    monsters: list = []
    monster_imgs: list = []
    message: Message
    battle_status_windows: list = []
    font = None
    get_exp = 0
    scenes = None
    screen = None
    flg = 0
    attack_lv = 1
    order=[]
    active = 0
    start = False

    def __init__(self, players: list, monsters: list, current_scene: int, scenes, screen: Surface) -> None:
        self.current_scene = current_scene
        self.players = players
        self.monsters = monsters
        self.message = Message("", True)
        self.command_win = CommandWindow(Command.BATTLE_SELECT, scene.SW - 25, 48, 12.5, scene.SH / 6)
        self.battle_status_windows = [BattleStatusWindow() for _ in players]
        self.monster_imgs = [mapimgdata.load_img(f"imgs/monsters/{monster.img}", -1, False) for monster in monsters]
        for idx, img in enumerate(self.monster_imgs):
            w = 120
            h = img.get_height() * (w / img.get_width())
            self.monster_imgs[idx] = pygame.transform.scale(img, (w, h))
        self.font = pygame.font.Font("fonts/PixelMplus10-Regular.ttf", 24)
        self.scenes=scenes
        self.screen = screen
        self.order = self.sort()

        
        for _,player in enumerate(self.players):
            for i,_ in enumerate(player.flgs):
                player.flgs[i] = 0
        

    def remove_monster(self, remove_index):
        self.monsters.remove(self.monsters[remove_index])
        self.monster_imgs.remove(self.monster_imgs[remove_index])

    def back_to_current_scene(self, scenes):
        scenes.scenes.remove(self)
        scenes.current_scene = self.current_scene

    def random(self, base:int)->int:#+-10%の乱数を生成
        tmp=math.floor(base/10)
        rand_value=random.randint(0,tmp)
        plus_minus=random.randint(1,2)
        if plus_minus==1:#1でbaseにプラス 2でマイナス
            base=base+rand_value
        else:
            base=base-rand_value
            if base<0:
                base=0
        return base
    
    def sort(self)->list:
        elements=len(self.players)+len(self.monsters)
        order=[0 for _ in range(elements)]
        for i,player in enumerate(self.players):
            order[i] = player
        for i,monster in enumerate(self.monsters):
            order[i+len(self.players)] = monster
        
        for i,_ in enumerate(order):
            for j,_ in enumerate(order):
                if len(order)-1 <= j:
                    break
                if order[j].agility < order[j+1].agility:
                    order[j], order[j+1] = order[j+1], order[j]
        return order

    def next(self):
        self.order = self.sort()
        self.active +=1
        if self.active > len(self.order)-1:
            self.active = 0


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

        self.message.event()
        if True in [player.name == self.order[self.active].name for player in self.players]:
            (is_operate, is_close, cmd) = self.command_win.event()
            if self.order[self.active].flgs[0] == 1:
                self.order[self.active].flgs[0] = 0
                self.message.msg += self.order[self.active].name+"は防御を解いた\n"
            if not self.message.msg.endswith(("ターン")):
                self.message.msg += "\n" + self.order[self.active].name + "のターン"
            if "index" in cmd:
                if cmd["unique"] == "battle_select":
                    self.flg = 0
                    if cmd["index"] == 0: #攻撃
                        self.command_win.set_commands(Command.NONE, "to_monster", [monster.name for monster in self.monsters])
                    elif cmd["index"] == 1: #魔法
                        self.command_win.set_commands(Command.NONE, "magic", ["ボラギ","ボラギノ","ボラギノル","ボラギノール"])
                    elif cmd["index"]==2: #特技

                        pass
                    elif cmd["index"]==3: #道具
                        pass
                    elif cmd["index"]==4: #防御
                        self.order[self.active].flgs[0] = 1
                        self.message.msg = self.order[self.active].name+"は防御している\n"
                        self.next()
                    elif cmd["index"]==5: #逃げる
                        self.back_to_current_scene(scenes)
                        return
                elif cmd["unique"] == "to_monster":
                    if self.flg == 0:
                        self.message.msg=""
                        self.attack(self.order[self.active], self.monsters[cmd["index"]])
                    elif self.flg == 1:
                        self.magic_attack(self.order[self.active], self.monsters[cmd["index"]], self.attack_lv)
                    print(self.order[self.active].name)
                    self.next()
                    self.command_win.set_commands(Command.BATTLE_SELECT)
                elif cmd["unique"] == "magic":
                    self.message.msg=""
                    self.flg = 1
                    if cmd["index"] == 0:
                        self.attack_lv = 1
                        self.message.msg = "ボラギ"
                    elif cmd["index"] == 1:
                        self.attack_lv = 1.4
                        self.message.msg="ボラギノ"
                    elif cmd["index"] == 2:
                        self.attack_lv = 1.8
                        self.message.msg="ボラギノル"
                    elif cmd["index"] == 3:
                        self.attack_lv = 2.5
                        self.message.msg="ボラギノール"
                    self.command_win.set_commands(Command.NONE, "to_monster", [monster.name for monster in self.monsters])
        else:
            print(self.order[self.active].name)
            random.seed()
            tonum = random.randint(0, len(self.players)-1)
            cmdnum = random.randint(1,1000)
            if cmdnum <= 800:
                self.attack(self.order[self.active], self.players[tonum])
            elif cmdnum <= 1000:
                self.message.msg += "  " + self.order[self.active].name + "はボーッとしている\n"
            self.next()
            pass

        clock.tick(scenes.FPS)
        pygame.display.flip()
        
    def draw(self, scenes, screen: Surface):
        pygame.Surface.fill(screen, (0, 0, 0))
        self.message.draw(screen)
        self.command_win.draw(screen)
        for idx, battle_status_window in enumerate(self.battle_status_windows):
            battle_status_window.draw(screen, idx * scene.SW / 4, self.players[idx].name, self.players[idx].hp, self.players[idx].mp, self.players[idx].maxhp, self.players[idx].maxmp)
        x = scene.SW / 2 - (len(self.monsters) * 140) / 2
        for idx, monster_img in enumerate(self.monster_imgs):
            text = self.font.render(self.monsters[idx].name, True, color.WHITE)
            screen.blit(
                monster_img,
                (x + idx * 140, scene.SH / 3)
            )
            screen.blit(
                text,
                (x + idx * 140, (scene.SH / 3 + 140 + (26 if idx % 2 == 1 else 0)))
            )

    def attack(self, _from, _to, attack_lv:int = 1):
        dmg = math.floor(self.random(_from.power*attack_lv))
        if True in [player.name == self.order[self.active].name for player in self.players]:
            pass
        else:
            if _to.flgs[0] == 1:
                dmg = math.floor(dmg / 2)
        _to.hp -= dmg
        if _to.hp<0:
            _to.hp=0
        if True in [player.name == self.order[self.active].name for player in self.players]:
            self.message.msg += _from.name+"は" + _to.name+"に" + str(dmg) + "ダメージ与えた\n"
        else:
            self.message.msg += "  " + _from.name + "は" + _to.name + "に" + str(dmg) + "ダメージ与えた\n"
        self.hp_check()
        return

    def magic_attack(self, _from, _to, attack_lv:int = 1):
        dmg=math.floor(self.random(_from.m_power*attack_lv))
        _to.hp -= dmg
        if _to.hp<0:
            _to.hp=0
        temp = self.message.msg
        self.message.msg = _from.name+"は"+temp+"を使った\n"+_to.name+"に"+str(dmg)+"ダメージ与えた\n"
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
            self.draw(self.scenes, self.screen)
            self.message.draw_until_press_key(self.screen)
            self.players[0].money+=self.get_exp
            for player in self.players:
                player.exp+=self.get_exp
            print(f"{self.players[0].money},{self.players[0].exp}")
            self.back_to_current_scene(self.scenes)
        return