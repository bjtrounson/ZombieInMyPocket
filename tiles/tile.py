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
    _tile_sides: [AbstractTileSide]
    _x: float
    _y: float

    def __init__(self, tile_type: TileType, x: float, y: float):
        self.tile_type = tile_type
        self._x = x
        self._y = y
        match tile_type:
            case TileType.Foyer:
                self.tile_name = "Foyer"
                self.tile_behaviour = DefaultBehaviour()
                self._tile_sides = [Door(TilePosition.North), Wall(TilePosition.East), Wall(TilePosition.South),
                                    Wall(TilePosition.West)]
            case TileType.Bedroom:
                self.tile_name = "Bedroom"
                self.tile_behaviour = DefaultBehaviour()
            case TileType.DiningRoom:
                self.tile_name = "Dining Room"
                self.tile_behaviour = DefaultBehaviour()
            case TileType.FamilyRoom:
                self.tile_name = "Family Room"
                self.tile_behaviour = DefaultBehaviour()
            case TileType.Bathroom:
                self.tile_name = "Bathroom"
                self.tile_behaviour = DefaultBehaviour()
            case TileType.Kitchen:
                self.tile_name = "Kitchen"
                self.tile_behaviour = KitchenBehaviour()
            case TileType.Storage:
                self.tile_name = "Storage"
                self.tile_behaviour = StorageBehaviour()
            case TileType.EvilTemple:
                self.tile_name = "Evil Temple"
                self.tile_behaviour = EvilTempleBehaviour()
            case TileType.Patio:
                self.tile_name = "Patio"
                self.tile_behaviour = DefaultBehaviour()
            case TileType.Yard1 | TileType.Yard2 | TileType.Yard3:
                self.tile_name = "Yard"
                self.tile_behaviour = DefaultBehaviour()
            case TileType.Garage:
                self.tile_name = "Garage"
                self.tile_behaviour = DefaultBehaviour()
            case TileType.SittingArea:
                self.tile_name = "Sitting Area"
                self.tile_behaviour = DefaultBehaviour()
            case TileType.Garden:
                self.tile_name = "Garden"
                self.tile_behaviour = GardenBehaviour()
            case TileType.Graveyard:
                self.tile_name = "Graveyard"
                self.tile_behaviour = GraveyardBehaviour()

    def rotate_tile(self, rotation_direction: RotationDirection) -> None:
        north_side = self._tile_sides[self.get_door_index_from_position(TilePosition.North)]
        east_side = self._tile_sides[self.get_door_index_from_position(TilePosition.East)]
        south_side = self._tile_sides[self.get_door_index_from_position(TilePosition.South)]
        west_side = self._tile_sides[self.get_door_index_from_position(TilePosition.West)]
        if rotation_direction is RotationDirection.Right:
            self._tile_sides[self.get_door_index_from_position(TilePosition.North)] = west_side
            self._tile_sides[self.get_door_index_from_position(TilePosition.East)] = north_side
            self._tile_sides[self.get_door_index_from_position(TilePosition.South)] = east_side
            self._tile_sides[self.get_door_index_from_position(TilePosition.West)] = south_side
        elif rotation_direction is RotationDirection.Left:
            self._tile_sides[self.get_door_index_from_position(TilePosition.North)] = east_side
            self._tile_sides[self.get_door_index_from_position(TilePosition.West)] = north_side
            self._tile_sides[self.get_door_index_from_position(TilePosition.South)] = west_side
            self._tile_sides[self.get_door_index_from_position(TilePosition.East)] = south_side

    def get_door_index_from_position(self, door_position: TilePosition) -> int:
        for i in range(len(self._tile_sides)):
            side: AbstractTileSide = self._tile_sides[i]
            if side.get_tile_side() == door_position:
                return i

    def get_side_from_index(self, index: int) -> AbstractTileSide:
        return self._tile_sides[index]

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_tile_sides(self) -> [AbstractTileSide]:
        return self._tile_sides
