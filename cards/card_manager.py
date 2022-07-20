from builders.card_builder import CardBuilder
from cards.card import Card
from items.item_type import ItemType


class CardManager:
    _builder: CardBuilder
    _cards_deck: list[Card]

    def __init__(self):
        self._builder: CardBuilder = CardBuilder()
        self._cards_deck: list[Card] = []

    def add_all_cards(self):
        for item in range(len(ItemType)):
            self._builder.build_game_object(ItemType(item + 1))
            self._cards_deck.append(self._builder.get_card_object())

    def get_deck(self) -> list[Card]:
        return self._cards_deck
