import unittest
from level.level import Level, NoDoorNearError, TileExistsError
from player import Player
from tiles.tile import Tile
from tiles.tile_positions import TilePosition
from tiles.tile_type import TileType


class LevelTestCases(unittest.TestCase):
    def setUp(self) -> None:
        self.player: Player = Player(1, 6, [], 0, 0)

    def test_when_tile_is_added_tile_expect_count_go_up(self):
        level = Level([Tile(TileType.Foyer, 0, 0)], self.player)
        level.add_new_tile(Tile(TileType.Foyer, 0, 1))
        expected_count = 2
        actual_count = level.get_tile_count()
        self.assertEqual(expected_count, actual_count)

    def test_when_tile_is_added_where_no_doors_near_expect_exception_raised(self):
        with self.assertRaises(NoDoorNearError):
            level = Level([Tile(TileType.Foyer, 0, 0)], self.player)
            level.add_new_tile(Tile(TileType.Foyer, 0, -1))

    def test_when_tile_is_added_where_door_is_near_expect_no_exception_raised(self):
        raised = False
        try:
            level = Level([Tile(TileType.Foyer, 0, 0)], self.player)
            level.add_new_tile(Tile(TileType.Foyer, 0, 1))
        except NoDoorNearError:
            raised = True
        self.assertFalse(raised, "Exception raised")

    def test_when_tile_is_added_where_tile_already_exist_expect_exception_raised(self):
        with self.assertRaises(TileExistsError):
            level = Level([Tile(TileType.Foyer, 0, 0)], self.player)
            level.add_new_tile(Tile(TileType.Foyer, 0, 0))

    def test_when_tile_is_added_where_no_tile_exists_expect_no_exception_raised(self):
        raised = False
        try:
            level = Level([Tile(TileType.Foyer, 0, 0)], self.player)
            level.add_new_tile(Tile(TileType.Foyer, 0, 1))
        except NoDoorNearError:
            raised = True
        self.assertFalse(raised, "Exception raised")

    def test_when_tile_has_doors_expect_door_info(self):
        level = Level([Tile(TileType.Foyer, 0, 0)], self.player)
        expected_door_info: [dict[int, TilePosition]] = [{0, TilePosition.North}]
        actual_door_info: [dict[int, TilePosition]] = level.get_door_info_on_tile(level.get_tile_by_cords(0, 0))
        self.assertEqual(expected_door_info, actual_door_info)

    def test_when_get_tile_by_cords_expect_tile(self):
        tile = [Tile(TileType.Foyer, 0, 0)]
        level = Level(tile, self.player)
        expected_tile = tile[0]
        actual_tile = level.get_tile_by_cords(0, 0)
        self.assertEqual(expected_tile, actual_tile)

    def test_when_get_tile_by_cords_out_of_range_expect_false(self):
        tile = [Tile(TileType.Foyer, 0, 0)]
        level = Level(tile, self.player)
        expected_result = False
        actual_result = level.get_tile_by_cords(1, 0)
        self.assertEqual(expected_result, actual_result)

    def test_when_player_is_on_tile_expect_tile_player_is_on(self):
        tile = [Tile(TileType.Foyer, 0, 0)]
        level = Level(tile, self.player)
        expected_result = tile[0]
        actual_result = level.get_tile_player_is_on()
        self.assertEqual(expected_result, actual_result)


if __name__ == '__main__':
    unittest.main()
