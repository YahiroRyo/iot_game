import pygame
from event import KeyEvent
from context import Context
from pygame_ui.ui_radio_button import UIRadioButton

class UIRadioButtonList(KeyEvent):
    buttons: list = []
    callback = None

    def __init__(self, context: Context, button_texts: list, callback, pos: list, size: list):
        super().__init__(context)
        self.callback = callback
        for (idx, text) in enumerate(button_texts):
            self.buttons.append(
                UIRadioButton(
                    context,
                    idx,
                    self.radio_button_callback,
                    text,
                    (pos[0], pos[1] - idx * size[1] - idx * 10),
                    size
                )
            )
    
    def draw(self):
        for button in self.buttons:
            button.draw()

    def event(self, e: pygame.event.Event):
        for button in self.buttons:
            button.event(e)
        super().event(e)

    def radio_button_callback(self, switch: bool, id: int):
        self.callback(switch, id)
        for button in self.buttons:
            if button.id != id:
                button.switch = False
                button.update_color()