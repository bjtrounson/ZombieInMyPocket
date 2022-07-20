from builders.tile_builder import TileBuilder
from tiles.tile import Tile
from tiles.tile_type import TileType


class TileManager:
    _builder: TileBuilder
    _inner_tile_deck: list[Tile]
    _outer_tile_deck: list[Tile]

    def __init__(self):
        self._builder: TileBuilder = TileBuilder()
        self._inner_tile_deck: list[Tile] = []
        self._outer_tile_deck: list[Tile] = []

    def add_inner_tiles(self):
        for item in range(7):
            self._builder.build_game_object(TileType(item + 2))
            self._inner_tile_deck.append(self._builder.get_tile_object())

    def add_outer_tiles(self):
        for item in range(7):
            self._builder.build_game_object(TileType(item + 10))
            self._outer_tile_deck.append(self._builder.get_tile_object())

    def get_inner_tile_deck(self) -> list[Tile]:
        return self._inner_tile_deck

    def get_outer_tile_deck(self) -> list[Tile]:
        return self._outer_tile_deck

