from tiles.tile import Tile
from player import Player
from tiles.door import Door
from tiles.tile_positions import TilePosition
from tiles.wall import Wall


class TileExistsError(Exception):
    pass


class NoDoorNearError(Exception):
    pass


class Level:
    _tiles: list[Tile]
    _player: Player

    def __init__(self, tiles: list[Tile], player: Player):
        self._tiles = tiles
        self._player = player

    def add_new_tile(self, tile: Tile):
        if not self.check_if_tile_already_exists(tile.get_x(), tile.get_y()):
            if self.check_if_door_exist_near_cords(tile.get_x(), tile.get_y()):
                self._tiles.append(tile)
            else:
                raise NoDoorNearError("No doors near that location")
        else:
            raise TileExistsError("Tile already exists here")

    def check_if_tile_already_exists(self, x: float, y: float) -> bool:
        result = False
        if len(self._tiles) == 1:
            tile = self._tiles[0]
            if tile.get_x() == x and tile.get_y() == y:
                result = True
        else:
            for tile in self._tiles:
                if tile.get_x() == x and tile.get_y() == y:
                    result = True
        return result

    def check_if_door_exist_near_cords(self, x: float, y: float) -> bool:
        if self.check_if_tile_already_exists(x, y + 1):
            tile: Tile = self.get_tile_by_cords(x, y + 1)
            if type(tile.get_side_from_index(TilePosition.South.value)) is Door:
                return True
            else:
                return False
        elif self.check_if_tile_already_exists(x, y - 1):
            tile: Tile = self.get_tile_by_cords(x, y - 1)
            if type(tile.get_side_from_index(TilePosition.North.value)) is Door:
                return True
            else:
                return False
        elif self.check_if_tile_already_exists(x + 1, y):
            tile: Tile = self.get_tile_by_cords(x + 1, y)
            if type(tile.get_side_from_index(TilePosition.West.value)) is Door:
                return True
            else:
                return False
        elif self.check_if_tile_already_exists(x - 1, y):
            tile: Tile = self.get_tile_by_cords(x - 1, y)
            if type(tile.get_side_from_index(TilePosition.East.value)) is Door:
                return True
            else:
                return False
        else:
            return False

    def get_available_doors(self, tile: Tile) -> list[Door]:
        door_list: list[Door] = []
        for side_i in range(len(tile.get_tile_sides())):
            side = tile.get_tile_sides()[side_i]
            if type(side) is Door:
                door_position: TilePosition = TilePosition(side_i)
                match door_position:
                    case TilePosition.North:
                        if not self.check_if_tile_already_exists(tile.get_x(), tile.get_y() + 1):
                            door_list.append(side)
                    case TilePosition.South:
                        if not self.check_if_tile_already_exists(tile.get_x(), tile.get_y() - 1):
                            door_list.append(side)
                    case TilePosition.West:
                        if not self.check_if_tile_already_exists(tile.get_x() - 1, tile.get_y()):
                            door_list.append(side)
                    case TilePosition.East:
                        if not self.check_if_tile_already_exists(tile.get_x() + 1, tile.get_y()):
                            door_list.append(side)
        return door_list

    @staticmethod
    def get_walls_on_tile(tile: Tile) -> list[Wall]:
        wall_list: list[Wall] = []
        for side in tile.get_tile_sides():
            if type(side) is Wall:
                wall_list.append(side)
        return wall_list

    @staticmethod
    def get_door_info_on_tile(tile: Tile):
        door_info_list = []
        for side in tile.get_tile_sides():
            if type(side) is Door:
                door_info = {"door_index": int(tile.get_door_index_from_position(side.get_tile_side().value)),
                             "door_position": side.get_tile_side()}
                door_info_list.append(door_info)
        return door_info_list

    def get_tile_player_is_on(self) -> Tile:
        for tile in self._tiles:
            if tile.get_x() == self._player.get_x() and tile.get_y() == self._player.get_y():
                return tile

    def get_tile_by_cords(self, x: float, y: float) -> Tile | bool:
        for tile in self._tiles:
            if tile.get_x() == x and tile.get_y() == y:
                return tile
        return False

    def get_tile_count(self) -> int:
        return len(self._tiles)

    def get_player(self) -> Player:
        return self._player
