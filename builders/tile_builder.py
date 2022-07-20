from builders.abstract_game_object_builder import AbstractGameObjectBuilder
from tiles.default_behaviour import DefaultBehaviour
from tiles.door import Door
from tiles.evil_temple_behaviour import EvilTempleBehaviour
from tiles.garden_behaviour import GardenBehaviour
from tiles.graveyard_behaviour import GraveyardBehaviour
from tiles.kitchen_behaviour import KitchenBehaviour
from tiles.storage_behaviour import StorageBehaviour
from tiles.tile import Tile
from tiles.tile_positions import TilePosition
from tiles.tile_type import TileType
from tiles.wall import Wall


class TileBuilder(AbstractGameObjectBuilder):
    _tile: Tile

    def build_game_object(self, object_type: TileType):
        tile = Tile(object_type, 0, 0)
        match object_type:
            case TileType.Foyer:
                tile.tile_name = "Foyer"
                tile.tile_behaviour = DefaultBehaviour()
                tile._tile_sides = [Door(TilePosition.North), Wall(TilePosition.East), Wall(TilePosition.South),
                                    Wall(TilePosition.West)]
            case TileType.Bedroom:
                tile.tile_name = "Bedroom"
                tile.tile_behaviour = DefaultBehaviour()
                tile._tile_sides = [Door(TilePosition.North), Wall(TilePosition.East), Wall(TilePosition.South),
                                    Door(TilePosition.West)]
            case TileType.DiningRoom:
                tile.tile_name = "Dining Room"
                tile.tile_behaviour = DefaultBehaviour()
                tile._tile_sides = [Door(TilePosition.North), Door(TilePosition.East), Door(TilePosition.South),
                                    Door(TilePosition.West)]
            case TileType.FamilyRoom:
                tile.tile_name = "Family Room"
                tile.tile_behaviour = DefaultBehaviour()
                tile._tile_sides = [Door(TilePosition.North), Door(TilePosition.East), Wall(TilePosition.South),
                                    Door(TilePosition.West)]
            case TileType.Bathroom:
                tile.tile_name = "Bathroom"
                tile.tile_behaviour = DefaultBehaviour()
                tile._tile_sides = [Door(TilePosition.North), Wall(TilePosition.East), Wall(TilePosition.South),
                                    Wall(TilePosition.West)]
            case TileType.Kitchen:
                tile.tile_name = "Kitchen"
                tile.tile_behaviour = KitchenBehaviour()
                tile._tile_sides = [Door(TilePosition.North), Door(TilePosition.East), Wall(TilePosition.South),
                                    Door(TilePosition.West)]
            case TileType.Storage:
                tile.tile_name = "Storage"
                tile.tile_behaviour = StorageBehaviour()
                tile._tile_sides = [Door(TilePosition.North), Wall(TilePosition.East), Wall(TilePosition.South),
                                    Wall(TilePosition.West)]
            case TileType.EvilTemple:
                tile.tile_name = "Evil Temple"
                tile.tile_behaviour = EvilTempleBehaviour()
                tile._tile_sides = [Wall(TilePosition.North), Door(TilePosition.East), Wall(TilePosition.South),
                                    Door(TilePosition.West)]
            case TileType.Patio:
                tile.tile_name = "Patio"
                tile.tile_behaviour = DefaultBehaviour()
                tile._tile_sides = [Door(TilePosition.North), Door(TilePosition.East), Door(TilePosition.South),
                                    Wall(TilePosition.West)]
            case TileType.Yard1 | TileType.Yard2 | TileType.Yard3:
                tile.tile_name = "Yard"
                tile.tile_behaviour = DefaultBehaviour()
                tile._tile_sides = [Wall(TilePosition.North), Door(TilePosition.East), Door(TilePosition.South),
                                    Door(TilePosition.West)]
            case TileType.Garage:
                tile.tile_name = "Garage"
                tile.tile_behaviour = DefaultBehaviour()
                tile._tile_sides = [Wall(TilePosition.North), Wall(TilePosition.East), Door(TilePosition.South),
                                    Door(TilePosition.West)]
            case TileType.SittingArea:
                tile.tile_name = "Sitting Area"
                tile.tile_behaviour = DefaultBehaviour()
                tile._tile_sides = [Wall(TilePosition.North), Door(TilePosition.East), Door(TilePosition.South),
                                    Door(TilePosition.West)]
            case TileType.Garden:
                tile.tile_name = "Garden"
                tile.tile_behaviour = GardenBehaviour()
                tile._tile_sides = [Wall(TilePosition.North), Door(TilePosition.East), Door(TilePosition.South),
                                    Door(TilePosition.West)]
            case TileType.Graveyard:
                tile.tile_name = "Graveyard"
                tile.tile_behaviour = GraveyardBehaviour()
                tile._tile_sides = [Wall(TilePosition.North), Door(TilePosition.East), Door(TilePosition.South),
                                    Wall(TilePosition.West)]
        self._tile = tile

    def get_tile_object(self) -> Tile:
        return self._tile
