from abstract_tile_behaviour import TileBehaviour


class Tile:
    tile_name: str
    tile_behaviour: TileBehaviour

    def __init__(self, tile_name, tile_behaviour):
        self.tile_name = tile_name
        self.tile_behaviour = tile_behaviour
