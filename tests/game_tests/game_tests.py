import unittest

from builders.tile_builder import TileBuilder
from cards.card import Card
from cards.card_manager import CardManager
from game import Game
from level.level import Level
from player import Player
from tiles.door import Door
from tiles.tile import Tile
from tiles.tile_manager import TileManager
from tiles.tile_positions import TilePosition
from tiles.tile_type import TileType


class GameTestCases(unittest.TestCase):
    def setUp(self) -> None:
        self.card_manager: CardManager = CardManager()
        self.tile_manager: TileManager = TileManager()
        self.tile_builder: TileBuilder = TileBuilder()
        self.tile_manager.add_inner_tiles()
        self.tile_manager.add_outer_tiles()
        self.card_manager.add_all_cards()
        self.mock_inside_tiles: list[Tile] = self.tile_manager.get_inner_tile_deck()
        self.mock_outside_tiles = self.tile_manager.get_outer_tile_deck()
        self.tile_builder.build_game_object(TileType.Foyer)
        tiles: list[Tile] = [self.tile_builder.get_tile_object()]
        player: Player = Player(6, 1, 2, [], 0, 0)
        level = Level(tiles, player)
        self.tile_builder.build_game_object(TileType.EvilTemple)
        self.tile_builder.get_tile_object().set_pos(0, 1)
        self.new_tile: Tile = self.tile_builder.get_tile_object()
        self.game = Game(9, 11, level)

    def test_when_new_game_create_new_game(self):
        player: Player = Player(6, 1, 2, [], 0, 0)
        level = Level([Tile(TileType.Foyer, 0, 0)], player)
        game = Game(9, 11, level)
        self.assertEqual(game._time, 9)
        self.assertEqual(game._end_time, 11)
        self.assertEqual(game._level, level)
        self.assertIsInstance(game._card_manager, CardManager)
        self.assertIsInstance(game._current_dev_card, Card)
        self.assertIsInstance(game._dev_cards, list)

    def test_when_new_tile_given_expect_new_tiles_doors_available(self):
        expected_doors: list[Door] = [Door(TilePosition.East), Door(TilePosition.West)]
        actual_doors: list[Door] = self.game.get_tile_doors(self.new_tile)
        self.assertEqual(expected_doors, actual_doors)

    def test_when_door_in_east_position_then_rotated_expect_corrected_to_south_position(self):
        exit_door: Door = self.game.get_tile_doors(self.new_tile)[0]
        self.game.correct_tile_rotation(TilePosition.South, self.new_tile, exit_door)
        expected_door = exit_door
        actual_door = self.new_tile.get_tile_sides()[TilePosition.South.value]
        self.assertEqual(expected_door, actual_door)

    def test_when_door_in_west_position_then_rotated_expect_corrected_to_south_position(self):
        exit_door: Door = self.game.get_tile_doors(self.new_tile)[1]
        self.game.correct_tile_rotation(TilePosition.South, self.new_tile, exit_door)
        expected_door = exit_door
        actual_door = self.new_tile.get_tile_sides()[TilePosition.South.value]
        self.assertEqual(expected_door, actual_door)

    def test_when_player_inside_expect_inside_tile_to_be_draw(self):
        expected_tile: Tile = self.game._inside_tiles[0]
        actual_tile = self.game.draw_tile()
        self.assertEqual(expected_tile, actual_tile)

    def test_when_player_outside_expect_outside_tile_to_be_draw(self):
        self.game._level.get_player()._inside = False
        expected_tile: Tile = self.game._outside_tiles[0]
        actual_tile = self.game.draw_tile()
        self.assertEqual(expected_tile, actual_tile)

    def test_when_given_deck_of_dev_cards_expect_deck_to_be_in_different_order(self):
        dev_cards: list[Card] = self.card_manager.get_deck()
        expected_order = dev_cards
        actual_order = self.game.shuffle_decks(dev_cards)
        self.assertNotEqual(expected_order, actual_order)

    def test_when_give_deck_of_tiles_expect_deck_to_be_in_different_order(self):
        original_order = self.mock_inside_tiles
        actual_order = self.game.shuffle_decks(self.mock_inside_tiles)
        self.assertNotEqual(original_order, actual_order)

    def test_when_setup_expect_dev_cards_deck_length_less(self):
        expected_dev_cards: int = len(self.card_manager.get_deck())
        self.game.setup()
        actual_dev_cards: int = len(self.game._dev_cards)
        self.assertNotEqual(expected_dev_cards, actual_dev_cards)

    def test_when_setup_expect_current_dev_card_exists(self):
        self.game.setup()
        is_current_dev_card_exist = False
        if self.game._current_dev_card is not None:
            is_current_dev_card_exist = True
        self.assertTrue(is_current_dev_card_exist)

    def test_when_setup_expect_inside_tiles_shuffled(self):
        self.game.setup()
        original_order = self.mock_inside_tiles
        actual_order = self.game._inside_tiles
        self.assertNotEqual(original_order, actual_order)

    def test_when_setup_expect_outside_tiles_shuffled(self):
        self.game.setup()
        original_order = self.mock_outside_tiles
        actual_order = self.game._outside_tiles
        self.assertNotEqual(original_order, actual_order)

    def test_when_move_algorithm_inside_expect_inside_tile_deck_to_be_smaller(self):
        tile = self.game.draw_tile()
        tile.set_pos(0, 1)
        self.game.tile_algorithm(tile)
        expected_deck_count = 7
        actual_deck_count = len(self.game._inside_tiles)
        self.assertNotEqual(expected_deck_count, actual_deck_count)

    def test_when_move_algorithm_outside_expect_outside_tile_deck_to_be_smaller(self):
        self.game._level.get_player()._inside = False
        tile = self.game.draw_tile()
        tile.set_pos(0, 1)
        self.game.tile_algorithm(tile)
        expected_deck_count = 7
        actual_deck_count = len(self.game._outside_tiles)
        self.assertNotEqual(expected_deck_count, actual_deck_count)

    def test_when_move_algorithm_has_exception_tile_already_exists_expect_false(self):
        tile = self.game.draw_tile()
        result = self.game.tile_algorithm(tile)
        self.assertFalse(result)

    def test_when_move_algorithm_doesnt_have_exception_tile_already_exist_expect_true(self):
        tile = self.game.draw_tile()
        tile.set_pos(0, 1)
        result = self.game.tile_algorithm(tile)
        self.assertTrue(result)

    def test_when_move_algorithm_has_exception_no_doors_near_expect_false(self):
        tile = self.game.draw_tile()
        tile.set_pos(1, 0)
        result = self.game.tile_algorithm(tile)
        self.assertFalse(result)

    def test_when_move_algorithm_doesnt_have_exception_no_doors_near_expect_true(self):
        tile = self.game.draw_tile()
        tile.set_pos(0, 1)
        result = self.game.tile_algorithm(tile)
        self.assertTrue(result)

    def test_when_attack_zombie_count_is_lower_than_player_damage_expect_no_damage_taken(self):
        self.game.attack(1, self.game._level.get_player().get_attack_score())
        expected_health = 6
        actual_health = self.game._level.get_player().get_health()
        self.assertEqual(expected_health, actual_health)

    def test_when_attack_zombie_count_is_higher_than_player_damage_expect_damage_taken(self):
        self.game.attack(3, self.game._level.get_player().get_attack_score())
        expected_health = 4
        actual_health = self.game._level.get_player().get_health()
        self.assertEqual(expected_health, actual_health)

    def test_when_player_cowers_expect_player_to_go_up_by_three(self):
        self.game.cower()
        expected_health = 9
        actual_health = self.game._level.get_player().get_health()
        self.assertEqual(expected_health, actual_health)


if __name__ == '__main__':
    unittest.main()
