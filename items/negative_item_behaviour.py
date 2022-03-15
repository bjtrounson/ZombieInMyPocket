from items.abstract_item_behaviour import AbstractItemBehaviour


class NegativeItemBehaviour(AbstractItemBehaviour):
    damage: int

    def __init__(self, damage: int):
        self.damage = damage

    def action(self):
        return self.damage
