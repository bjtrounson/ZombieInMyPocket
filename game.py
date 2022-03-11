from player import Player
from tiles.tile import Tile
from cards.card import Card
from move_type import MoveType


class Game:
    time: int
    player: Player
    outdoor_tiles: list[Tile]
    indoor_tiles: list[Tile]
    dev_cards: list[Card]
    current_dev_cards: list[Card]
    current_dev_card: Card

    def __init__(self, time: int, player: Player, outdoor_tiles: list[Tile], indoor_tiles: list[Tile], dev_cards: list[Card], current_dev_cards: list[Card]):
        self.time = time
        self.player = player
        self.outdoor_tiles = outdoor_tiles
        self.indoor_tiles = indoor_tiles
        self.dev_cards = dev_cards
        self.current_dev_cards = current_dev_cards

    def shuffle(self):
        pass

    def move(self, move_direction: MoveType):
        pass

    def pickup_item(self):
        pass

    def attack(self, zombie_count: int, attack_score: int):
        pass

    def cower(self):
        self.player.health += 3
