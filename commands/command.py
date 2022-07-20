import cmd
import os

from builders.tile_builder import TileBuilder
from cards.card_manager import CardManager
from file_manager.file_manager import FileManager
from game import Game
from game_options import GameOptions
from level.level import Level
from parser import Parser
from pickle_manager.pickle_manager import PickleManager
from player import Player
from tiles.tile import Tile
from tiles.tile_type import TileType


class Command(cmd.Cmd):
    _game: Game
    _card_manager: CardManager
    _pickle_manager: PickleManager
    _file_manager: FileManager
    _game_options: GameOptions

    def __init__(self, cwd: str):
        super().__init__()
        parser = Parser()
        try:
            parser.add_args()
            self._game_options = GameOptions(parser.args.health, parser.args.damage, parser.args.item_limit,
                                             parser.args.start_time, parser.args.end_time)
        except ValueError as e:
            print(e)
            print("Applying defaults")
            self._game_options = GameOptions(6, 1, 2, 9, 11)
        player: Player = Player(self._game_options.player_health, self._game_options.player_damage,
                                self._game_options.player_item_limit, [], 0, 0)
        tile_builder = TileBuilder()
        tile_builder.build_game_object(TileType.Foyer)
        tiles: list[Tile] = [tile_builder.get_tile_object()]
        level = Level(tiles, player)
        self._game = Game(self._game_options.game_start_time, self._game_options.game_end_time, level)
        self._pickle_manager = PickleManager(cwd)
        self._file_manager = FileManager(cwd)


