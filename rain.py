import pygame
import random

class Rain:
    def __init__(self,win):
        self.x = random.uniform(0, 1280)
        self.y = -1
        self.yspeed = random.uniform(1,3)
        self.win = win
        self.length = random.uniform(10,20)

    def fall(self):
        self.y += self.yspeed

    def show(self):
        pygame.draw.rect(self.win,(0,0,255),(self.x,self.y,2,self.length))

def drawRain(rain):
    for water in rain:
        water.show()
        if water.y <= 720:
            water.fall()
        else:
            rain.pop(rain.index(water))

    pygame.display.update()