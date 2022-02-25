import pygame
from event import KeyEvent
from canvas import Canvas
from context import Context
from pygame_ui.ui_context_menu_radio_button import UIContextMenuRadioButton

class UIContextRadioButtonList(KeyEvent, Canvas):
    buttons: list = []
    callback = None

    def __init__(self, context: Context, button_texts: list, callback):
        super().__init__(context)
        self.callback = callback
        self.height = len(button_texts) * 42;
        for (idx, text) in enumerate(button_texts):
            self.buttons.append(
                UIContextMenuRadioButton(
                    context,
                    self.radio_button_callback,
                    text,
                    text,
                    idx
                )
            )
        self.buttons[0].switch = True
        self.buttons[0].update_color()
    
    def set_pos(self, x: int, y: int):
        super().set_pos(x, y)
        for (idx, button) in enumerate(self.buttons):
            button.set_pos(x, y + (idx * 42))

    def draw(self):
        for button in self.buttons:
            button.draw()

    def event(self, e: pygame.event.Event):
        for button in self.buttons:
            button.event(e)

    def radio_button_callback(self, switch: bool, id: int):
        self.callback(switch, id)
        for button in self.buttons:
            if button.id != id:
                button.switch = False
                button.update_color()