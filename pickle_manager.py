import os
import pickle

from cards.card_manager import CardManager
from game import Game
from level.level import Level
from player import Player
from tiles.tile import Tile
from tiles.tile_type import TileType


class NoFileNameError(Exception):
    pass


class PickleManager:
    def __init__(self):
        self._current_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def serialize_object_to_file(self, file_name: str, obj: Game) -> None:
        """

        :param file_name: str
        :param obj: Game
        :return: None

        >>> pickle_manager = PickleManager()
        >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> card_manager = CardManager()
        >>> card_manager.add_all_cards()
        >>> game = Game(9, level, card_manager.get_deck())
        >>> pickle_manager.serialize_object_to_file('test_save', game)
        """
        if file_name != '':
            with open(os.path.join(self._current_dir, f'{file_name}.pkl'), 'wb', 0) as f:
                pickle.dump(obj, f)
        else:
            raise NoFileNameError

    def deserialize_file_to_object(self, file_name: str) -> Game:
        """

        :param file_name: str
        :return: Game
        >>> pickle_manager = PickleManager()
        >>> pickle_manager.deserialize_file_to_object('test_save') #doctest: +ELLIPSIS
        <game.Game object at 0x...>
        """
        if file_name != '':
            with open(os.path.join(self._current_dir, f'{file_name}.pkl'), 'rb') as f:
                game = pickle.load(f)
            return game
        else:
            raise NoFileNameError

    def remove_save(self, file_name):
        """

        :param file_name: str
        :return:
        >>> pickle_manager = PickleManager()
        >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> card_manager = CardManager()
        >>> card_manager.add_all_cards()
        >>> game = Game(9, level, card_manager.get_deck())
        >>> pickle_manager.serialize_object_to_file('testing_save', game)
        >>> pickle_manager.remove_save('testing_save')
        """
        if os.path.exists(os.path.join(self._current_dir, f'{file_name}.pkl')):
            os.remove(os.path.join(self._current_dir, f'{file_name}.pkl'))
        else:
            raise FileNotFoundError

    def get_current_dir(self) -> str:
        return self._current_dir
