from items.item import Item


class Player:
    _health: int
    _attack: int
    _item_limit: int
    _player_items: list[Item]
    _inside: bool
    _x: float
    _y: float

    def __init__(self, health: int, attack: int, item_limit: int, player_items: list[Item], x: float, y: float):
        self._health = health
        self._attack = attack
        self._item_limit = item_limit
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

    def get_items(self) -> list[Item]:
        return self._player_items

    def add_item(self, item: Item):
        if len(self._player_items) >= self._item_limit:
            raise ValueError
        else:
            self._player_items.append(item)

    def replace_item(self, item_to_replace: Item, item: Item):
        self._player_items[self._player_items.index(item_to_replace)] = item

    def set_health(self, health: int):
        self._health = health

    def set_attack_score(self, attack_score: int):
        self._attack = attack_score

    def set_item_limit(self, item_limit: int):
        self._item_limit = item_limit

    def set_player_pos(self, x: float, y: float):
        self._x = x
        self._y = y
