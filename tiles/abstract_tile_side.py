from abc import ABC
from tiles.tile_positions import TilePosition


class AbstractTileSide(ABC):
    original_tile_side: TilePosition

    def __init__(self, tile_side: TilePosition):
        self.original_tile_side = tile_side

    def get_tile_side(self) -> TilePosition:
        return self.original_tile_side

    def __eq__(self, other):
        return self.original_tile_side == other
