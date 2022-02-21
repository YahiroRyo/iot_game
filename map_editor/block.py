import pygame
import config

class Block:
    name = ""
    img = None
    id = 0
    x = 0
    y = 0
    msize = config.MAP_MSIZE

    def __init__(self, name: str, img: str, id: int):
        self.name = name
        if img != "None":
            tmp = pygame.image.load(f"../imgs/{img}")
            self.img =  pygame.transform.scale(tmp, (self.msize, self.msize)).convert()
        else:
            self.img = None
        self.id = id
    
    def draw(self, screen: pygame.Surface):
        if self.img != None:
            screen.blit(
                self.img,
                (self.x, self.y)
            )
    
    def is_hit(self, x, y):
        return  self.x <= x                 and \
                self.x + self.msize >= x  and \
                self.y <= y               and \
                self.y + self.msize >= y