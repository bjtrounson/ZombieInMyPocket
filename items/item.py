from abstract_item_behaviour import AbstractItemBehaviour


class Item:
    item_name: str
    item_behaviour: AbstractItemBehaviour

    def __init__(self, item_name: str, item_behaviour: AbstractItemBehaviour):
        self.item_name = item_name
        self.item_behaviour = item_behaviour
