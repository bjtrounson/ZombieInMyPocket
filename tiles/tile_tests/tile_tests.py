import unittest
from tiles.tile import Tile
from tiles.tile_type import TileType
from tiles.tile_positions import TilePosition
from tiles.tile import RotationDirection


class TileTestCases(unittest.TestCase):
    def test_when_rotate_right_once_that_door_index_changes(self):
        tile = Tile(TileType.Foyer, 0, 0)
        tile.rotate_tile(RotationDirection.Right)
        expected_index = 1
        actual_index = tile.get_door_index_from_position(TilePosition.North.value)
        self.assertEqual(expected_index, actual_index)  # add assertion here

    def test_when_rotate_right_twice_that_door_index_changes(self):
        tile = Tile(TileType.Foyer, 0, 0)
        tile.rotate_tile(RotationDirection.Right)
        tile.rotate_tile(RotationDirection.Right)
        expected_index = 2
        actual_index = tile.get_door_index_from_position(TilePosition.North.value)
        self.assertEqual(expected_index, actual_index)

    def test_when_rotate_left_once_that_door_index_changes(self):
        tile = Tile(TileType.Foyer, 0, 0)
        tile.rotate_tile(RotationDirection.Left)
        expected_index = 3
        actual_index = tile.get_door_index_from_position(TilePosition.North.value)
        self.assertEqual(expected_index, actual_index)

    def test_when_rotate_left_twice_that_door_index_changes(self):
        tile = Tile(TileType.Foyer, 0, 0)
        tile.rotate_tile(RotationDirection.Left)
        tile.rotate_tile(RotationDirection.Left)
        expected_index = 2
        actual_index = tile.get_door_index_from_position(TilePosition.North.value)
        self.assertEqual(expected_index, actual_index)


if __name__ == '__main__':
    unittest.main()
