from items.item import Item
from items.genre import Genre

class Equipment(Item):
    def __init__(self, id: int, name: str, img: str, callback) -> None:
        super().__init__(id, name, img, callback)
        self.genre = Genre.EQUIPMENT