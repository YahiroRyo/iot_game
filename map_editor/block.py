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
        tmp = pygame.image.load(f"../imgs/{img}.png")
        self.name = name
        self.img =  pygame.transform.scale(tmp, (self.msize, self.msize)).convert()
        self.id = id
    
    def draw(self, screen: pygame.Surface):
        screen.blit(
            self.img,
            (self.x, self.y)
        )
    
    def is_hit(self, x, y):
        return  self.x <= x                 and \
                self.x + self.msize >= x  and \
                self.y <= y               and \
                self.y + self.msize >= y