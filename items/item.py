from items.abstract_item_behaviour import AbstractItemBehaviour
from items.passive_item_behaviour import PassiveItemBehaviour
from items.positive_item_behaviour import PositiveItemBehaviour
from items.negative_item_behaviour import NegativeItemBehaviour
from items.item_type import ItemType


class Item:
    item_name: str
    primary_item_behaviour: AbstractItemBehaviour
    optional_item_behaviour: AbstractItemBehaviour | None = None
    combo_item: ItemType | None = None
    second_combo_item: ItemType | None = None
    uses: int | None = None
    item_type: ItemType

    def __init__(self, item_type: ItemType):
        self.item_type = item_type
        match item_type:
            case ItemType.Oil:
                self.item_name = "Oil"
                self.primary_item_behaviour = PassiveItemBehaviour()
                self.optional_item_behaviour = NegativeItemBehaviour(6)
                self.combo_item = ItemType.Candle
                self.uses = 1
            case ItemType.Gasoline:
                self.item_name = "Gasoline"
                self.primary_item_behaviour = NegativeItemBehaviour(6)
                self.optional_item_behaviour = PassiveItemBehaviour()
                self.combo_item = ItemType.Candle
                self.second_combo_item = ItemType.Chainsaw
                self.uses = 1
            case ItemType.BoardWNail:
                self.item_name = "Board w/ Nails"
                self.primary_item_behaviour = NegativeItemBehaviour(1)
            case ItemType.CanOfSoda:
                self.item_name = "Can of Soda"
                self.primary_item_behaviour = PositiveItemBehaviour(2)
            case ItemType.GrislyFemur:
                self.item_name = "Grisly Femur"
                self.primary_item_behaviour: NegativeItemBehaviour(1)
            case ItemType.GolfClub:
                self.item_name = "Golf Club"
                self.primary_item_behaviour = NegativeItemBehaviour(1)
            case ItemType.Candle:
                self.item_name = "Candle"
                self.primary_item_behaviour = NegativeItemBehaviour(6)
                self.optional_item_behaviour = NegativeItemBehaviour(6)
                self.combo_item = ItemType.Oil
                self.second_combo_item = ItemType.Gasoline
            case ItemType.Chainsaw:
                self.item_name = "Chainsaw"
                self.primary_item_behaviour = NegativeItemBehaviour(3)
                self.optional_item_behaviour = PassiveItemBehaviour()
                self.combo_item = ItemType.Gasoline
                self.uses = 2

    def action(self):
        if self.uses is not None:
            self.uses -= 1
        return self.primary_item_behaviour.action()
