class Context:
    players: list
    monsters: list

    def __init__(self, players: list = [], monsters: list = []) -> None:
        self.players = players
        self.monsters = monsters