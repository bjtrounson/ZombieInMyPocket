import os.path
import unittest

from cards.card import Card
from cards.card_manager import CardManager
from game import Game
from level.level import Level
from pickle_manager.pickle_manager import PickleManager, NoFileNameError
from player import Player
from tiles.tile import Tile
from tiles.tile_type import TileType


class PickleManagerTestCases(unittest.TestCase):
    def setUp(self) -> None:
        self.current_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.pickle_manager = PickleManager(self.current_dir)
        self.card_manager: CardManager = CardManager()
        self.card_manager.add_all_cards()
        tiles: list[Tile] = [Tile(TileType.Foyer, 0, 0)]
        player: Player = Player(6, 1, 2, [], 0, 0)
        level = Level(tiles, player)
        self.game = Game(9, 11, level)
        self.file_name = 'testing_save'

    def test_when_remove_file_expect_file_to_not_exist(self):
        self.pickle_manager.serialize_object_to_file(self.file_name, self.game)
        self.pickle_manager.remove_save(self.file_name)
        expected = False
        actual = os.path.isfile(os.path.join(self.current_dir, f'{self.file_name}.pkl'))
        self.assertEqual(expected, actual)

    def test_when_save_file_expect_file_in_game_dir(self):
        if os.path.exists(os.path.join(self.current_dir, f'{self.file_name}.pkl')):
            self.pickle_manager.remove_save(self.file_name)
        self.pickle_manager.serialize_object_to_file(self.file_name, self.game)
        expected = True
        actual = os.path.isfile(os.path.join(self.current_dir, f'{self.file_name}.pkl'))
        self.assertEqual(expected, actual)

    def test_when_load_game_from_file_expect_game_state_to_be_same_as_file_with_the_player_having_more_health(self):
        if os.path.exists(os.path.join(self.current_dir, f'{self.file_name}.pkl')):
            self.pickle_manager.remove_save(self.file_name)
        self.game.cower()
        self.pickle_manager.serialize_object_to_file(self.file_name, self.game)
        self._reset_game()
        self.game = self.pickle_manager.deserialize_file_to_object(self.file_name)
        expected_health = 9
        actual_health = self.game._level.get_player().get_health()
        self.assertEqual(expected_health, actual_health)

    def _reset_game(self):
        tiles = [Tile(TileType.Foyer, 0, 0)]
        player = Player(6, 1, 2, [], 0, 0)
        level = Level(tiles, player)
        self.game = Game(9, 11, level)


if __name__ == '__main__':
    unittest.main()
