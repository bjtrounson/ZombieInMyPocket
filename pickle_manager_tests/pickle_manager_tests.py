import os.path
import unittest

from cards.card import Card
from cards.card_manager import CardManager
from game import Game
from level.level import Level
from pickle_manager import PickleManager, NoFileNameError
from player import Player
from tiles.tile import Tile
from tiles.tile_type import TileType


class PickleManagerTestCases(unittest.TestCase):
    def setUp(self) -> None:
        self.pickle_manager = PickleManager()
        self.current_dir = self.pickle_manager.get_current_dir()
        self.card_manager: CardManager = CardManager()
        self.card_manager.add_all_cards()
        dev_cards: list[Card] = self.card_manager.get_deck()
        tiles: list[Tile] = [Tile(TileType.Foyer, 0, 0)]
        player: Player = Player(6, 1, [], 0, 0)
        level = Level(tiles, player)
        self.game = Game(9, level, dev_cards)
        self.file_name = 'testing_save'

    def test_when_remove_file_expect_file_to_not_exist(self):
        self.pickle_manager.serialize_object_to_file(self.file_name, self.game)
        self.pickle_manager.remove_save(self.file_name)
        expected = False
        actual = os.path.isfile(os.path.join(self.current_dir, f'{self.file_name}.pkl'))
        self.assertEqual(expected, actual)

    def test_when_remove_file_that_doesnt_exist_expect_no_file_error_raised(self):
        with self.assertRaises(FileNotFoundError):
            self.pickle_manager.remove_save('mnrkerothnsdkfnsekfjseinfwkejkfowefnikw')

    def test_when_save_file_expect_file_in_game_dir(self):
        if os.path.exists(os.path.join(self.current_dir, f'{self.file_name}.pkl')):
            self.pickle_manager.remove_save(self.file_name)
        self.pickle_manager.serialize_object_to_file(self.file_name, self.game)
        expected = True
        actual = os.path.isfile(os.path.join(self.current_dir, f'{self.file_name}.pkl'))
        self.assertEqual(expected, actual)

    def test_when_save_file_with_no_file_name_expect_no_file_name_error_raised(self):
        with self.assertRaises(NoFileNameError):
            self.pickle_manager.serialize_object_to_file('', self.game)

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

    def test_when_load_from_file_with_no_file_name_expect_no_file_name_error_raised(self):
        with self.assertRaises(NoFileNameError):
            self.pickle_manager.deserialize_file_to_object('')

    def _reset_game(self):
        cards = self.card_manager.get_deck()
        tiles = [Tile(TileType.Foyer, 0, 0)]
        player = Player(6, 1, [], 0, 0)
        level = Level(tiles, player)
        self.game = Game(9, level, cards)


if __name__ == '__main__':
    unittest.main()
