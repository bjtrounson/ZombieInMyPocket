from items.item import Item


class Player:
    _health: int
    _attack: int
    _player_items: list[Item]
    _inside: bool
    _x: float
    _y: float

    def __init__(self, health: int, attack: int, player_items: list[Item], x: float, y: float):
        self._health = health
        self._attack = attack
        self._player_items = player_items
        self._x = x
        self._y = y
        self._inside = True

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_health(self) -> int:
        return self._health

    def get_is_inside(self) -> bool:
        return self._inside

    def get_attack_score(self) -> int:
        return self._attack

    def set_health(self, health: int):
        self._health = health

    def set_player_pos(self, x: float, y: float):
        self._x = x
        self._y = y
