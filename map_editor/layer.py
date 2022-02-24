import pygame
import config
from map import Map
from context import Context
from event import KeyEvent
from block_data import BLOCKS, get_block_index_from_id
import json
from pygame_ui.ui_context_menu_checkbox import UIContextMenuCheckbox
from pygame_ui.ui_context_menu_text import UIContextMenuText
from pygame_ui.ui_input import UIInput
from pygame_ui.ui_window import UIWindow
from ui import UI

class Layer(KeyEvent):
    # マップレイヤー
    map: Map = None
    everything: Map = None
    npcs: Map = None

    # マップを隠すフラグ
    hidden_map = False
    hidden_everything = False
    hidden_npcs = False

    is_put = False
    is_scroll = False
    x = 0
    y = 0
    prev_x = 0
    prev_y = 0
    current_map = 0

    context_uis = []
    context_uis_pos = None

    def __init__(self, context: Context):
        super().__init__(context)
        context.set("BLOCKS", BLOCKS)
        self.context_uis_pos = UIContextMenuText(context, "")
        self.context_uis = [
            self.context_uis_pos,
            UIContextMenuCheckbox(context, self.add_sea_event, "乗船イベントを追加", "乗船イベントを追加"),
            UIContextMenuCheckbox(context, self.add_land_event, "降船イベントを追加", "降船イベントを追加"),
            UIContextMenuCheckbox(context, self.add_move_to_other_map_event, "他のマップへ遷移", "他のマップへ遷移"),
        ]
        map_keys = [
            "map_main",
            "map_everything",
            "map_npcs",
        ]
        if config.MAP_IS_LOAD:
            with open(f"../maps/{config.MAP_NAME}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                config.MAP_HEIGHT = len(data["map_main"])
                config.MAP_WIDTH = len(data["map_main"][0])
                config.MAP_CONF = data["conf"]
                for (idx, key) in enumerate(map_keys):
                    blocks = []
                    if key in data:
                        blocks = data[key]
                    # マップエディタとの互換性がなかった場合
                    # ※ map_mainのkey必須
                    if len(blocks) == 0:
                        for _ in range(config.MAP_WIDTH):
                            blocks_w = []
                            for _ in range(config.MAP_HEIGHT):
                                blocks_w.append(-1)
                            blocks.append(blocks_w)
                    else:
                        for (idx_y, block_h) in enumerate(blocks):
                            for (idx_x, block_idx) in enumerate(block_h):
                                blocks[idx_y][idx_x] = get_block_index_from_id(block_idx)
                    if idx == 0: self.map = Map(context, blocks)
                    if idx == 1: self.everything = Map(context, blocks)
                    if idx == 2: self.npcs = Map(context, blocks)
                if "events" in data:
                    for key in data["events"]:
                        context.events[key] = data["events"][key]
        else:
            bg = -1
            for (idx, block) in enumerate(BLOCKS):
                if block.id == config.MAP_BG_ID:
                    bg = idx
                    break
            for (idx, _) in enumerate(map_keys):
                blocks = []
                for _ in range(config.MAP_WIDTH):
                    blocks_w = []
                    for _ in range(config.MAP_HEIGHT):
                        blocks_w.append(bg)
                    blocks.append(blocks_w)
                if idx == 0: self.map = Map(context, blocks)
                if idx == 1: self.everything = Map(context, blocks)
                if idx == 2: self.npcs = Map(context, blocks)
                bg = -1

    def draw(self):
        if self.map != None and not self.hidden_map: self.map.draw() 
        if self.everything != None and not self.hidden_everything: self.everything.draw()
        if self.npcs != None and not self.hidden_npcs: self.npcs.draw()
        if self.context.current_mode == 1 and self.context.current_select_block[0] != -1:
            pygame.draw.rect(self.context.screen, (255, 0, 0), (
                    self.context.current_select_block[1] * config.MAP_MSIZE + self.x +  self.context.get("SW") / 3,
                    self.context.current_select_block[0] * config.MAP_MSIZE + self.y,
                    config.MAP_MSIZE,
                    config.MAP_MSIZE
                ),
                5
            )
            
    def set_pos(self, x: int, y: int):
        if self.map != None:
            self.map.x = x
            self.map.y = y
        if self.everything != None:
            self.everything.x = x
            self.everything.y = y
        if self.npcs != None:
            self.npcs.x = x
            self.npcs.y = y

    def set_x(self, x: int):
        if self.map != None: self.map.x = x
        if self.everything != None: self.everything.x = x
        if self.npcs != None: self.npcs.x = x

    def set_y(self, y: int):
        if self.map != None: self.map.y = y
        if self.everything != None: self.everything.y = y
        if self.npcs != None: self.npcs.y = y

    def mouse_down_right(self, context: Context):
        (x, y) = pygame.mouse.get_pos()
        self.is_scroll = True
        self.prev_x = self.x - x
        self.prev_y = self.y - y

    def mouse_up_right(self, context: Context):
        self.is_scroll = False

    def mouse_down_left(self, context: Context):
        if context.get("CONTEXT_MENU").is_active and context.get("CONTEXT_MENU").is_hit(): return
        if context.get("UI").is_active_input_window: return
        (x, y) = pygame.mouse.get_pos()
        if context.current_block != -1 and context.current_mode == 0 and x >= context.get("SW") / 3:
            self.is_put = True
        if  context.current_mode == 0 and context.current_select_block[0] != -1:
            context.current_select_block = (-1, -1)
            context.get("CONTEXT_MENU").pop()
        elif context.current_mode == 1:
            if context.current_select_block[0] == -1:
                self.context_uis_pos.text = f"{int((x - self.x) / config.MAP_MSIZE) * config.MAP_MSIZE} {int((y - self.y) / config.MAP_MSIZE) * config.MAP_MSIZE}"
                context.get("CONTEXT_MENU").push(self.context_uis)
            context.current_select_block = [int((y - self.y) / config.MAP_MSIZE), int((x - self.x - self.context.get("SW") / 3) / config.MAP_MSIZE)]
            key = ""
            if self.current_map == 0: key = "map_main"
            if self.current_map == 1: key = "map_everything"
            if self.current_map == 2: key = "map_npcs"
            for ui in self.context_uis:
                try:
                    ui.switch = False
                    ui.update_color()
                except:
                    pass
            text_x = int((x - self.x - self.context.get("SW") / 3) / config.MAP_MSIZE) * config.MAP_MSIZE
            text_y = int((y - self.y) / config.MAP_MSIZE) * config.MAP_MSIZE
            self.context_uis_pos.text = f"{text_x} {text_y}"
                    
            for event in self.context.events[key]:
                if "pos" in event and event["pos"] == self.context.get_current_select_block() and event["name"] == "to_sea":
                    self.context_uis[1].switch = True
                    self.context_uis[1].update_color()
                if "pos" in event and event["pos"] == self.context.get_current_select_block() and event["name"] == "to_land":
                    self.context_uis[2].switch = True
                    self.context_uis[2].update_color()
                if "from_pos" in event and event["from_pos"] == self.context.get_current_select_block() and event["name"] == "to_other_map":
                    self.context_uis[3].switch = True
                    self.context_uis[3].update_color()

    def mouse_up_left(self, context: Context):
        self.is_put = False
    
    def after_event(self, context: Context):
        (x, y) = pygame.mouse.get_pos()
        if self.is_put:
            try:
                if self.current_map == 0:
                    self.map.blocks[int((y - self.y) / config.MAP_MSIZE )][int((x - self.x - self.context.get("SW") / 3) / config.MAP_MSIZE)] = context.current_block
                    self.map.update_blocks()
                if self.current_map == 1:
                    self.everything.blocks[int((y - self.y) / config.MAP_MSIZE )][int((x - self.x - self.context.get("SW") / 3) / config.MAP_MSIZE)] = context.current_block
                    self.everything.update_blocks()
                if self.current_map == 2:
                    self.npcs.blocks[int((y - self.y) / config.MAP_MSIZE )][int((x - self.x - self.context.get("SW") / 3) / config.MAP_MSIZE)] = context.current_block
                    self.npcs.update_blocks()
            except:
                pass
            
        if self.is_scroll:
            self.x = self.prev_x + x
            self.y = self.prev_y + y
            self.set_pos(self.x, self.y)

    def add_sea_event(self, switch: bool):
        try:
            key = self.context.get_current_map(self.current_map)
            if switch:
                self.context.events[key].append({
                    "name": "to_sea",
                    "pos": self.context.get_current_select_block()
                })
            else:
                for (idx, event) in enumerate(self.context.events[key]):
                    if event["name"] == "to_sea" and event["pos"] == self.context.current_select_block:
                        self.context.events[key].pop(idx)
        except:
            pass
    def add_land_event(self, switch: bool):
        try:
            key = self.context.get_current_map(self.current_map)
            if switch:
                self.context.events[key].append({
                    "name": "to_land",
                    "pos": self.context.get_current_select_block()
                })
            else:
                for (idx, event) in enumerate(self.context.events[key]):
                    if event["name"] == "to_land" and event["pos"] == self.context.current_select_block:
                        self.context.events[key].pop(idx)
        except:
            pass

    def add_move_to_other_map_event(self, switch: bool):
        if switch:
            input_window: UIWindow = self.context.get("INPUT_WINDOW")
            input_window.init([
                UIInput(
                    self.context,
                    (input_window.x + input_window.width / 2 - 200, input_window.y + input_window.height / 2 - 50),
                    400,
                    "マップ名"
                ),
                UIInput(
                    self.context,
                    (input_window.x + input_window.width / 2 - 200, input_window.y + input_window.height / 2 + 20),
                    400,
                    "遷移先座標 x y空白区切り"
                )
            ], "遷移先のマップ名を入力")
            ui: UI = self.context.get("UI")
            ui.is_active_input_window = True
            ui.submit_callback = self.submit_add_move_to_other_map_event
            ui.close_callback = lambda: None
        else:
            key = self.context.get_current_map(self.current_map)
            for (idx, event) in enumerate(self.context.events[key]):
                print(event["from_pos"])
                if event["name"] == "to_other_map" and event["from_pos"] == self.context.get_current_select_block():
                    self.context.events[key].pop(idx)

    
    def submit_add_move_to_other_map_event(self, uis: list):
        # 遷移先のマップ名
        other_map_name = uis[0].text
        # 遷移先の位置
        pos = uis[1].text.split(" ")
        x = int(pos[0])
        y = int(pos[1])

        self.context.events[self.context.get_current_map(self.current_map)].append({
            "name": "to_other_map",
            "other_map_name": other_map_name,
            "from_pos": self.context.get_current_select_block(),
            "pos": [x, y]
        })