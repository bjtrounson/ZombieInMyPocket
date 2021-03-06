from tiles.abstract_tile_side import AbstractTileSide
from tiles.tile_positions import TilePosition


class Door(AbstractTileSide):

    def __init__(self, tile_side: TilePosition):
        super().__init__(tile_side)
