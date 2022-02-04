from items.genre import Genre

class Item:
    id = 0
    genre = Genre.ITEM
    name = ""
    img = ""
    callback = None
    def __init__(self, id: int, name: str, img: str, callback) -> None:
        self.id = id
        self.name = name
        self.img = img
        self.callback = callback