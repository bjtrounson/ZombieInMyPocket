from items.item import Item


class Player:
    health: int
    attack: int
    player_items: list[Item]

    def __init__(self, health: int, attack: int, player_items: list[Item]):
        self.health = health
        self.attack = attack
        self.player_items = player_items
