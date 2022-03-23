from tiles.tile import Tile
from player import Player
from tiles.door import Door
from tiles.tile_positions import TilePosition


class TileExistsError(Exception):
    pass


class NoDoorNearError(Exception):
    pass


class Level:
    _tiles: list[Tile]
    _player: Player

    def __init__(self, tiles: list[Tile]):
        self._tiles = tiles

    def add_new_tile(self, tile: Tile):
        try:
            if not self.check_if_tile_already_exists(tile.get_x(), tile.get_y()):
                if self.check_if_door_exist_near_cords(tile.get_x(), tile.get_y()):
                    self._tiles.append(tile)
                else:
                    raise NoDoorNearError()
            else:
                raise TileExistsError()
        except TileExistsError as e:
            print(f"Tile already exists here! :( {e}")
        except NoDoorNearError as e:
            print(f"No doors near that location! :( {e}")

    def check_if_tile_already_exists(self, x: float, y: float) -> bool:
        if len(self._tiles) < 2:
            tile = self._tiles[0]
            if tile.get_x() == x and tile.get_y() == y:
                return True
            else:
                return False
        else:
            for tile in self._tiles:
                if tile.get_x() == x and tile.get_y() == y:
                    return True
                else:
                    return False

    def check_if_door_exist_near_cords(self, x: float, y: float) -> bool:
        for tile in self._tiles:
            if tile.get_x() == (x - 1) and tile.get_y() == y:
                if type(tile.get_side_from_index(1)) is Door:
                    return True
            elif tile.get_x() == (x + 1) and tile.get_y() == y:
                if type(tile.get_side_from_index(3)) is Door:
                    return True
            elif tile.get_y() == (y - 1) and tile.get_x() == x:
                if type(tile.get_side_from_index(0)) is Door:
                    return True
            elif tile.get_y() == (y + 1) and tile.get_x() == x:
                if type(tile.get_side_from_index(2)) is Door:
                    return True
            else:
                return False

    @staticmethod
    def get_door_info_on_tile(tile: Tile) -> [dict[int, TilePosition]]:
        door_info_list: [dict[int, TilePosition]] = []
        for side in tile.get_tile_sides():
            if type(side) is Door:
                door_info = {tile.get_door_index_from_position(side.get_tile_side()), side.get_tile_side()}
                door_info_list.append(door_info)
        return door_info_list

    def get_tile_player_is_on(self) -> Tile:
        for tile in self._tiles:
            if tile.get_x() == self._player.get_x() and tile.get_y == self._player.get_y():
                return tile

    def get_tile_by_cords(self, x: float, y: float) -> Tile | bool:
        for tile in self._tiles:
            if tile.get_x() == x and tile.get_y() == y:
                return tile
        return False

    def get_tile_count(self) -> int:
        return len(self._tiles)