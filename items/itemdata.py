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

items = [
    Item("0101", "やくそう", "1人のhpを30回復 ", 10, item_0101),
    Item("0102", "すごいやくそう", "1人のhpを60回復 ", 100, item_0102),
    Item("0103", "やばいやくそう", "1人のhpを120回復 ", 600, item_0103),
]