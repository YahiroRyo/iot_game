from items.item import Item
from context import Context

def item_0101(context: Context):
    context.players[0].hp += 30
    if context.players[0].maxhp <= context.players[0].hp: context.players[0].hp = context.players[0].maxhp

def item_0102(context: Context):
    context.players[0].hp += 60
    if context.players[0].maxhp <= context.players[0].hp: context.players[0].hp = context.players[0].maxhp

def item_0103(context: Context):
    context.players[0].hp += 120
    if context.players[0].maxhp <= context.players[0].hp: context.players[0].hp = context.players[0].maxhp

def item_0104(context: Context):
    context.players[0].mp += 20
    if context.players[0].maxmp <= context.players[0].mp: context.players[0].mp = context.players[0].maxmp

def item_0105(context: Context):
    context.players[0].mp += 50
    if context.players[0].maxmp <= context.players[0].mp: context.players[0].mp = context.players[0].maxmp

def item_0106(context: Context):
    context.players[0].mp += 100
    if context.players[0].maxmp <= context.players[0].mp: context.players[0].mp = context.players[0].maxmp

items = [
    Item("0101", "やくそう", "1人のhpを30回復 ", 10, item_0101),
    Item("0102", "すごいやくそう", "1人のhpを60回復 ", 100, item_0102),
    Item("0103", "やばいやくそう", "1人のhpを120回復 ", 600, item_0103),
    Item("0104", "マジックパウダー", "1人のmpを20回復 ", 30, item_0104),
    Item("0103", "マジックストーン", "1人のmpを50回復 ", 200, item_0105),
    Item("0103", "マジックブック", "1人のmpを100回復 ", 800, item_0106),
]