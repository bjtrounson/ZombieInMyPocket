import unittest
from level.level import Level, NoDoorNearError
from tiles.tile import Tile
from tiles.tile_type import TileType


class LevelTestCases(unittest.TestCase):
    def test_when_tile_is_added_tile_expect_count_go_up(self):
        level = Level([Tile(TileType.Foyer, 0, 0)])
        level.add_new_tile(Tile(TileType.Foyer, 0, 1))
        expected_count = 2
        actual_count = level.get_tile_count()
        self.assertEqual(expected_count, actual_count)

    def test_when_tile_is_added_where_no_doors_near_expect_exception_raised(self):
        level = Level([Tile(TileType.Foyer, 0, 0)])
        self.assertRaises(NoDoorNearError, level.add_new_tile, Tile(TileType.Foyer, 0, -1))


if __name__ == '__main__':
    unittest.main()
