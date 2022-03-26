import argparse
import cmd
import doctest

from parser import Parser
from cards.card_manager import CardManager
from game import Game
from level.level import Level
from pickle_manager import PickleManager
from player import Player
from tiles.tile import Tile
from tiles.tile_type import TileType


class Main(cmd.Cmd):
    _game: Game
    _card_manager: CardManager
    _pickle_manager: PickleManager

    def __init__(self):
        super().__init__()
        parser = Parser()
        player: Player = Player(parser.args.health, parser.args.damage, [], 0, 0)
        tiles: list[Tile] = [Tile(TileType.Foyer, 0, 0)]
        level = Level(tiles, player)
        self._card_manager = CardManager()
        self._card_manager.add_all_cards()
        self._game = Game(9, level, self._card_manager.get_deck())
        self._pickle_manager = PickleManager()

    def do_save_game(self, file_name: str):
        """save_game [file_name] Saves the current Game state"""
        if file_name != '':
            self._pickle_manager.serialize_object_to_file(file_name, self._game)
        else:
            print("You need a file name!! 'save_game [file_name] Try Again'")

    def do_load_game(self, file_name: str) -> None:
        """load_game [file_name] Loads Game state from a file and makes it the current game"""
        if file_name != '':
            self._game = self._pickle_manager.deserialize_file_to_object(file_name)
        else:
            print("You need a file name!! 'load_game [file_name] Try Again")

    def do_EOF(self, line):
        """Exit"""
        return True


if __name__ == '__main__':
    Main().cmdloop()
