from cards.abstract_time_behaviour import AbstractTimeBehaviour
from items.item import Item


class ItemTimeBehaviour(AbstractTimeBehaviour):
    item: Item

    def __init__(self, message: str, item: Item):
        super().__init__(message)
        self.item = item

    def action(self):
        return self.item