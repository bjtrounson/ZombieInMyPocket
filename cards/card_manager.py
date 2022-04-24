from cards.bad_time_behaviour import BadTimeBehaviour
from cards.card import Card
from cards.good_time_behaviour import GoodTimeBehaviour
from cards.item_time_behaviour import ItemTimeBehaviour
from cards.neutral_time_behaviour import NeutralTimeBehaviour
from cards.passive_bad_time_behaviour import PassiveBadTimeBehaviour
from cards.time_action import TimeAction
from items.item import Item
from items.item_type import ItemType


class CardManager:
    _cards_deck: list[Card]

    def __init__(self):
        self._cards_deck: list[Card] = []

    def add_card(self, item_type: ItemType):
        match item_type:
            case ItemType.Oil:
                time_actions = [TimeAction(9, NeutralTimeBehaviour("You try hard not to wet yourself")),
                                TimeAction(10, ItemTimeBehaviour("ITEM", Item(ItemType.Oil))),
                                TimeAction(11, BadTimeBehaviour(6, "6 Zombies")),
                                ]
                card = Card(time_actions)
                self._cards_deck.append(card)
            case ItemType.Gasoline:
                time_actions = [TimeAction(9, BadTimeBehaviour(4, "4 Zombies")),
                                TimeAction(10, PassiveBadTimeBehaviour(1, "You sense your impending doom. -1 Health")),
                                TimeAction(11, ItemTimeBehaviour("ITEM", Item(ItemType.Gasoline))),
                                ]
                card = Card(time_actions)
                self._cards_deck.append(card)
            case ItemType.BoardWNail:
                time_actions = [TimeAction(9, ItemTimeBehaviour("ITEM", Item(ItemType.BoardWNail))),
                                TimeAction(10, BadTimeBehaviour(4, "4 Zombies")),
                                TimeAction(11, PassiveBadTimeBehaviour(1, "Something icky in your mouth. -1 Health")),
                                ]
                card = Card(time_actions)
                self._cards_deck.append(card)
            case ItemType.Machete:
                time_actions = [TimeAction(9, BadTimeBehaviour(4, "4 Zombies")),
                                TimeAction(10, PassiveBadTimeBehaviour(1, "A bat poops in your eye. -1 Health")),
                                TimeAction(11, BadTimeBehaviour(6, "6 Zombies")),
                                ]
                card = Card(time_actions)
                self._cards_deck.append(card)
            case ItemType.GrislyFemur:
                time_actions = [TimeAction(9, ItemTimeBehaviour("ITEM", Item(ItemType.GrislyFemur))),
                                TimeAction(10, BadTimeBehaviour(5, "5 Zombies")),
                                TimeAction(11, PassiveBadTimeBehaviour(1, "Your soul isn't wanted here")),
                                ]
                card = Card(time_actions)
                self._cards_deck.append(card)
            case ItemType.GolfClub:
                time_actions = [TimeAction(9, PassiveBadTimeBehaviour(1, "Slip on nasty goo. -1 Health")),
                                TimeAction(10, BadTimeBehaviour(4, "4 Zombies")),
                                TimeAction(11, NeutralTimeBehaviour("The smell of blood is in the air")),
                                ]
                card = Card(time_actions)
                self._cards_deck.append(card)
            case ItemType.Chainsaw:
                time_actions = [TimeAction(9, BadTimeBehaviour(3, "3 Zombies")),
                                TimeAction(10, NeutralTimeBehaviour("You hear terrible screams")),
                                TimeAction(11, BadTimeBehaviour(5, "5 Zombies")),
                                ]
                card = Card(time_actions)
                self._cards_deck.append(card)
            case ItemType.CanOfSoda:
                time_actions = [TimeAction(9, GoodTimeBehaviour("Candybar in your pocket. +1 Health", 1)),
                                TimeAction(10, ItemTimeBehaviour("ITEM", Item(ItemType.CanOfSoda))),
                                TimeAction(11, BadTimeBehaviour(6, "6 Zombies")),
                                ]
                card = Card(time_actions)
                self._cards_deck.append(card)
            case ItemType.Candle:
                time_actions = [TimeAction(9, NeutralTimeBehaviour("Your body shivers involuntarily")),
                                TimeAction(10, GoodTimeBehaviour("You feel a spark of hope. +1 Health", 1)),
                                TimeAction(11, BadTimeBehaviour(4, "4 Zombies")),
                                ]
                card = Card(time_actions)
                self._cards_deck.append(card)

    def add_all_cards(self):
        for item in range(len(ItemType)):
            self.add_card(ItemType(item + 1))

    def get_deck(self) -> list[Card]:
        return self._cards_deck
