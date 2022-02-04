from items.item import Item
from context import Context

def item_001(context: Context):
    for player in context.players:
        player.hp += 10000
        if player.maxhp <= player.hp: player.hp = player.maxhp

items = [
    Item(0, "薬草", "", item_001)
]