from context import Context
from traceback import print_exception
from items.genre import Genre

class Item:
    id = ""
    genre = Genre.ITEM
    name = ""
    img = ""
    instructions = ""
    price = 0
    hook = None
    def __init__(self, id: str, name: str, instructions, price : int, callback, img: str = "") -> None:
        self.id = id
        self.name = name
        self.img = img
        self.instructions = instructions
        self.price = price
        self.hook = callback
    
    def callback(self, context: Context):
        self.hook(context)
