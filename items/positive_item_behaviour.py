from items.abstract_item_behaviour import AbstractItemBehaviour


class PositiveItemBehaviour(AbstractItemBehaviour):
    health: int

    def __init__(self, health: int):
        self.health = health

    def action(self):
        return self.health