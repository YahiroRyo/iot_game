import math
import random

class Params:
    name=""             #名前
    hp=0
    mp=0
    power=0             #物理攻撃
    m_power=0           #魔法攻撃
    defense=0           #物理防御
    m_defense=0         #魔法防御
    agility=0           #素早さ
    luck=0              #会心率
    attack_times=1      #行動回数
    exp=0               #経験値

class Monster(Params):
    img=""              #モンスター画像
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


    def __init__(self, data:list) -> None:
        self.img=data[0]
        self.name=data[1]
        self.hp=self.random(data[2])
        self.mp=self.random(data[3])
        self.power=self.random(data[4])
        self.m_power=self.random(data[5])
        self.defense=self.random(data[6])
        self.m_defense=self.random(data[7])
        self.agility=self.random(data[8])
        self.luck=self.random(data[9])
        self.attack_times=self.random(data[10])
        self.exp=data[11]
        self.debug()

    def debug(self):
        print(f"{self.img}, {self.name}, {self.hp}, {self.mp}, {self.power}, {self.m_power}, {self.defense}, {self.m_defense}, {self.agility}, {self.luck}, {self.attack_times}, {self.exp}")