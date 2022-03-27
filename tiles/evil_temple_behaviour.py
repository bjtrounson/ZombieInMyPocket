from items.item import Item
from items.item_type import ItemType
from tiles.abstract_tile_behaviour import TileBehaviour


class EvilTempleBehaviour(TileBehaviour):

    def action(self) -> Item:
        return Item(ItemType.Totem)
