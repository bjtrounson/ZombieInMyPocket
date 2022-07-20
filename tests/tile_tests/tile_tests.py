import unittest

from builders.tile_builder import TileBuilder
from tiles.tile_type import TileType
from tiles.tile_positions import TilePosition
from tiles.tile import RotationDirection


class TileTestCases(unittest.TestCase):
    def setUp(self) -> None:
        self._tile_builder = TileBuilder()
        self._tile_builder.build_game_object(TileType.Foyer)
        self.tile = self._tile_builder.get_tile_object()
        
    def test_when_rotate_right_once_that_door_index_changes(self):
        self.tile.rotate_tile(RotationDirection.Right)
        expected_index = 1
        actual_index = self.tile.get_door_index_from_position(TilePosition.North.value)
        self.assertEqual(expected_index, actual_index)  # add assertion here

    def test_when_rotate_right_twice_that_door_index_changes(self):
        self.tile.rotate_tile(RotationDirection.Right)
        self.tile.rotate_tile(RotationDirection.Right)
        expected_index = 2
        actual_index = self.tile.get_door_index_from_position(TilePosition.North.value)
        self.assertEqual(expected_index, actual_index)

    def test_when_rotate_left_once_that_door_index_changes(self):
        self.tile.rotate_tile(RotationDirection.Left)
        expected_index = 3
        actual_index = self.tile.get_door_index_from_position(TilePosition.North.value)
        self.assertEqual(expected_index, actual_index)

    def test_when_rotate_left_twice_that_door_index_changes(self):
        self.tile.rotate_tile(RotationDirection.Left)
        self.tile.rotate_tile(RotationDirection.Left)
        expected_index = 2
        actual_index = self.tile.get_door_index_from_position(TilePosition.North.value)
        self.assertEqual(expected_index, actual_index)


if __name__ == '__main__':
    unittest.main()
