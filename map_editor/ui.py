import pygame
from context import Context
from pygame_ui.ui_title import UITitle
from pygame_ui.ui_checkbox import UICheckbox
from pygame_ui.ui_radio_button_list import UIRadioButtonList
from pygame_ui.ui_context_menu import UIContextMenu
from pygame_ui.ui_context_menu_checkbox import UIContextMenuCheckbox
from pygame_ui.ui_context_menu_radio_button_list import UIContextRadioButtonList

class UI:
    context: Context = None

    hidden_title: UITitle = None
    hidden_map_checkbox: UICheckbox = None
    hidden_everything_checkbox: UICheckbox = None
    hidden_npcs_checkbox: UICheckbox = None

    radio_button_list_title: UITitle = None
    radio_button_list: UIRadioButtonList = None

    context_menu: UIContextMenu = None

    def __init__(self, context: Context) -> None:
        self.context = context
        self.hidden_map_checkbox = UICheckbox(
            context,
            self.hidden_map,
            "layer1: メインマップを表示する",
            "layer1: メインマップを非表示にする",
            (10, context.get("SH") - 40),
            (30, 30)
        )
        self.hidden_everything_checkbox = UICheckbox(
            context,
            self.hidden_everything,
            "layer2: フリーマップを表示する",
            "layer2: フリーマップを非表示にする",
            (10, context.get("SH") - 80),
            (30, 30)
        )
        self.hidden_npcs_checkbox = UICheckbox(
            context,
            self.hidden_npcs,
            "layer3: NPCSマップを表示する",
            "layer3: NPCSマップを非表示にする",
            (10, context.get("SH") - 120),
            (30, 30)
        )
        self.hidden_title = UITitle(context, "非表示・表示", (10, context.get("SH") - 180), (0, 0, 0))

        self.radio_button_list = UIRadioButtonList(context, [
                "layer1: メインマップ",
                "layer2: フリーマップ",
                "layer3: NPCSマップ",
            ],
            self.radio_button_list_callback,
            (10, context.get("SH") - 240),
            (30, 30)
        )
        self.radio_button_list.buttons[0].switch = True
        self.radio_button_list.buttons[0].update_color()
        self.radio_button_list_title = UITitle(context, "操作するマップ", (10, context.get("SH") - 380), (0, 0, 0))

        self.context_menu = UIContextMenu(context, [
            UIContextRadioButtonList(self.context, [
                "設置モード",
                "選択モード",
            ], self.change_current_mode)
        ])
        self.context.set("CONTEXT_MENU", self.context_menu)

    def draw(self):
        self.hidden_map_checkbox.draw()
        self.hidden_everything_checkbox.draw()
        self.hidden_npcs_checkbox.draw()
        self.hidden_title.draw()
        self.radio_button_list.draw()
        self.radio_button_list_title.draw()
        self.context_menu.draw()

    def radio_button_list_callback(self, switch, current_button: int):
        if switch:
            self.context.layer.current_map = current_button
        else:
            self.context.layer.current_map = -1

    def hidden_map(self, switch: bool):
        self.context.layer.hidden_map = switch

    def hidden_everything(self, switch: bool):
        self.context.layer.hidden_everything = switch

    def hidden_npcs(self, switch: bool):
        self.context.layer.hidden_npcs = switch

    def context_checkbox_callback(self, switch: bool):
        pass

    def change_current_mode(self, switch: bool, id: int):
        if not switch:
            self.context.current_mode = -1
        self.context.current_mode = id

    def event(self, e: pygame.event.Event):
        self.context_menu.event(e)
        self.hidden_map_checkbox.event(e)
        self.hidden_everything_checkbox.event(e)
        self.hidden_npcs_checkbox.event(e)
        self.radio_button_list.event(e)