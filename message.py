from pygame.surface import Surface
from window import Window
import scene

class Message(Window):
    msg = ""
    is_operate = False

    def __init__(self, msg: str, is_operate: bool) -> None:
        super().__init__()
        self.msg = msg
        self.is_operate = is_operate

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
        return self.is_operate