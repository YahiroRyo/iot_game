from pygame.surface import Surface
from window import Window
import scene

class Message(Window):
    msg = ""

    def __init__(self, msg: str) -> None:
        super().__init__()
        self.msg = msg

    def draw(self, screen: Surface):
        self._draw(
            screen,
            scene.SW - 50,
            scene.SH / 3,
            25,
            scene.SH - scene.SH / 3 - 25
        )
        self._draw_str(screen, self.msg)
    
    def event(self):
        pass