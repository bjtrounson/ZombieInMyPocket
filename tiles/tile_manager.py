from tiles.tile import Tile


class TileManager:
    outdoor_tiles: [Tile]
    indoor_tiles: [Tile]
    current_level: [Tile]

    def __init__(self, outdoor_tiles: [Tile], indoor_tiles: [Tile]):
        self.outdoor_tiles = outdoor_tiles
        self.indoor_tiles = indoor_tiles
        self.current_level
