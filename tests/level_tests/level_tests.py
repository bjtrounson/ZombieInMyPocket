import unittest

from builders.tile_builder import TileBuilder
from level.level import Level, NoDoorNearError, TileExistsError
from player import Player
from tiles.tile import Tile, RotationDirection
from tiles.tile_positions import TilePosition
from tiles.tile_type import TileType


class LevelTestCases(unittest.TestCase):
    def setUp(self) -> None:
        self.player: Player = Player(1, 6, 2, [], 0, 0)
        self.tile_builder = TileBuilder()
        self.tile_builder.build_game_object(TileType.Foyer)
        self.tiles: list[Tile] = [self.tile_builder.get_tile_object()]

    def test_when_tile_is_added_tile_expect_count_go_up(self):
        level = Level(self.tiles, self.player)
        self.tile_builder.build_game_object(TileType.Foyer)
        self.tile_builder.get_tile_object().set_pos(0, 1)
        level.add_new_tile(self.tile_builder.get_tile_object())
        expected_count = 2
        actual_count = level.get_tile_count()
        self.assertEqual(expected_count, actual_count)

    def test_when_tile_is_added_where_no_doors_near_expect_exception_raised(self):
        with self.assertRaises(NoDoorNearError):
            level = Level(self.tiles, self.player)
            self.tile_builder.build_game_object(TileType.Foyer)
            self.tile_builder.get_tile_object().set_pos(0, -1)
            level.add_new_tile(self.tile_builder.get_tile_object())

    def test_when_tile_is_added_where_door_is_near_expect_no_exception_raised(self):
        raised = False
        try:
            level = Level(self.tiles, self.player)
            self.tile_builder.build_game_object(TileType.Foyer)
            self.tile_builder.get_tile_object().set_pos(0, 1)
            level.add_new_tile(self.tile_builder.get_tile_object())
        except NoDoorNearError:
            raised = True
        self.assertFalse(raised, "Exception raised")

    def test_when_tile_is_added_where_tile_already_exist_expect_exception_raised(self):
        with self.assertRaises(TileExistsError):
            level = Level(self.tiles, self.player)
            self.tile_builder.build_game_object(TileType.Foyer)
            self.tile_builder.get_tile_object().set_pos(0, 0)
            level.add_new_tile(self.tile_builder.get_tile_object())

    def test_when_tile_has_doors_expect_door_info(self):
        level = Level(self.tiles, self.player)
        expected_door_info = [{"door_index": 0, "door_position": TilePosition.North}]
        actual_door_info = level.get_door_info_on_tile(level.get_tile_by_cords(0, 0))
        self.assertEqual(expected_door_info, actual_door_info)

    def test_when_get_tile_by_cords_expect_tile(self):
        level = Level(self.tiles, self.player)
        expected_tile = self.tiles[0]
        actual_tile = level.get_tile_by_cords(0, 0)
        self.assertEqual(expected_tile, actual_tile)

    def test_when_get_tile_by_cords_out_of_range_expect_false(self):
        level = Level(self.tiles, self.player)
        expected_result = False
        actual_result = level.get_tile_by_cords(1, 0)
        self.assertEqual(expected_result, actual_result)

    def test_when_player_is_on_tile_expect_tile_player_is_on(self):
        level = Level(self.tiles, self.player)
        expected_result = self.tiles[0]
        actual_result = level.get_tile_player_is_on()
        self.assertEqual(expected_result, actual_result)

    def test_when_tile_is_next_to_other_tile_expect_tile_to_exists(self):
        self.tile_builder.build_game_object(TileType.Storage)
        self.tile_builder.get_tile_object().set_pos(0, 1)
        self.tiles.append(self.tile_builder.get_tile_object())
        level = Level(self.tiles, self.player)
        expected_result = True
        actual_result = level.check_if_tile_already_exists(0, 1)
        self.assertEqual(expected_result, actual_result)

    def test_when_no_tile_is_next_to_other_tile_expect_no_tile_to_exist(self):
        level = Level(self.tiles, self.player)
        expected_result = False
        actual_result = level.check_if_tile_already_exists(1, 0)
        self.assertEqual(expected_result, actual_result)

    def test_when_adding_multiple_tiles(self):
        level = Level(self.tiles, self.player)
        new_tiles = []
        self.tile_builder.build_game_object(TileType.DiningRoom)
        self.tile_builder.get_tile_object().set_pos(0, 1)
        new_tiles.append(self.tile_builder.get_tile_object())
        self.tile_builder.build_game_object(TileType.Bedroom)
        self.tile_builder.get_tile_object().set_pos(0, 2)
        new_tiles.append(self.tile_builder.get_tile_object())
        raised = False
        try:
            level.add_new_tile(new_tiles[0])
            level.add_new_tile(new_tiles[1])
        except NoDoorNearError:
            raised = True
        except TileExistsError:
            raised = True
        self.assertFalse(raised, "Exception raised")

    def test_when_no_doors_available_on_tile_expect_empty_list(self):
        self.tile_builder.build_game_object(TileType.Storage)
        self.tile_builder.get_tile_object().set_pos(0, 1)
        self.tiles.append(self.tile_builder.get_tile_object())
        level = Level(self.tiles, self.player)
        self.tiles[1].rotate_tile(RotationDirection.Right)
        self.tiles[1].rotate_tile(RotationDirection.Right)
        expected_result = []
        actual_result = level.get_available_doors(self.tiles[1])
        self.assertEqual(expected_result, actual_result)

    def test_when_doors_available_on_tile_expect_list_of_doors(self):
        self.tile_builder.build_game_object(TileType.Bedroom)
        self.tile_builder.get_tile_object().set_pos(0, 1)
        self.tiles.append(self.tile_builder.get_tile_object())
        level = Level(self.tiles, self.player)
        expected_result = [self.tiles[1].get_tile_sides()[0], self.tiles[1].get_tile_sides()[3]]
        actual_result = level.get_available_doors(self.tiles[1])
        self.assertEqual(expected_result, actual_result)


if __name__ == '__main__':
    unittest.main()
