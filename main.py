from pprint import pprint
import argparse

from cards.card import Card
from cards.card_manager import CardManager
from game import Game
from items.item_type import ItemType
from level.level import Level
from player import Player
from tiles.tile import Tile
from tiles.tile_type import TileType
card_manager = CardManager()
card_manager.add_all_cards()

parser = argparse.ArgumentParser(description='Zombie In My Pocket Game, in Python.')
parser.add_argument("-hp", "--health", type=int, help="Change starting player health", default=6)
parser.add_argument("-dmg", "--damage", type=int, help="Change starting player attack damage", default=3)
args = parser.parse_args()
if args.health < 1 or args.damage < 1:
    raise ValueError('Player stats cannot be less than 1')

player = Player(args.health,args.damage,[],0,0)
# card_manager.add_card(ItemType([1,2]))

print(player.get_attack_score())
print(player.get_health())
level = Level([], player)
game = Game(9, level, card_manager.get_deck())




print(card_manager.get_deck())
pprint(vars(card_manager.get_deck()[0]))