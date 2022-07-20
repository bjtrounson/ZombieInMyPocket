from tiles.abstract_tile_behaviour import TileBehaviour
from tiles.abstract_tile_side import AbstractTileSide
from tiles.tile_type import TileType
from tiles.default_behaviour import DefaultBehaviour
from tiles.evil_temple_behaviour import EvilTempleBehaviour
from tiles.kitchen_behaviour import KitchenBehaviour
from tiles.storage_behaviour import StorageBehaviour
from tiles.garden_behaviour import GardenBehaviour
from tiles.graveyard_behaviour import GraveyardBehaviour
from tiles.door import Door
from tiles.wall import Wall
from tiles.tile_positions import TilePosition
from enum import Enum


class RotationDirection(Enum):
    Right = 1
    Left = 2


class Tile:
    tile_name: str
    tile_type: TileType
    tile_behaviour: TileBehaviour
    _tile_sides: list[AbstractTileSide]
    _x: float
    _y: float

    def __init__(self, tile_type: TileType, x: float, y: float):
        self.tile_type = tile_type
        self._x = x
        self._y = y

    def _change_tile_side(self, tile_position: TilePosition, side) -> None:
        self._tile_sides[tile_position.value] = side
        
    def rotate_tile(self, rotation_direction: RotationDirection) -> None:
        north_side = self._tile_sides[TilePosition.North.value]
        east_side = self._tile_sides[TilePosition.East.value]
        south_side = self._tile_sides[TilePosition.South.value]
        west_side = self._tile_sides[TilePosition.West.value]
        if rotation_direction is RotationDirection.Right:
            self._change_tile_side(TilePosition.North, west_side)
            self._change_tile_side(TilePosition.East, north_side)
            self._change_tile_side(TilePosition.South, east_side)
            self._change_tile_side(TilePosition.West, south_side)
        elif rotation_direction is RotationDirection.Left:
            self._change_tile_side(TilePosition.North, east_side)
            self._change_tile_side(TilePosition.West, north_side)
            self._change_tile_side(TilePosition.South, west_side)
            self._change_tile_side(TilePosition.East, south_side)

    def get_door_index_from_position(self, door_position: int) -> int:
        for i in range(len(self._tile_sides)):
            side: AbstractTileSide = self._tile_sides[i]
            if side.get_tile_side() == TilePosition(door_position):
                return i

    def get_side_from_index(self, index: int) -> AbstractTileSide:
        return self._tile_sides[index]

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def set_pos(self, x: float, y: float):
        self._x = x
        self._y = y

    def get_tile_sides(self) -> [AbstractTileSide]:
        return self._tile_sides

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return NotImplemented
        return self.tile_name == other.tile_name and \
            self.tile_behaviour == other.tile_behaviour and \
            self.tile_type == other.tile_type and \
            self._tile_sides == other._tile_sides and \
            self._x == other._x and \
            self._y == other._y
