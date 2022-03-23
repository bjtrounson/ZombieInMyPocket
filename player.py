from items.item import Item


class Player:
    _health: int
    _attack: int
    _player_items: [Item]
    _x: float
    _y: float

    def __init__(self, health: int, attack: int, player_items: [Item], x: float, y: float):
        self._health = health
        self._attack = attack
        self._player_items = player_items
        self._x = x
        self._y = y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y
