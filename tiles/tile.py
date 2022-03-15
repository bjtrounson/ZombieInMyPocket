from tiles.abstract_tile_behaviour import TileBehaviour
from tiles.tile_type import TileType
from tiles.default_behaviour import DefaultBehaviour
from tiles.evil_temple_behaviour import EvilTempleBehaviour
from tiles.kitchen_behaviour import KitchenBehaviour
from tiles.storage_behaviour import StorageBehaviour
from tiles.garden_behaviour import GardenBehaviour
from tiles.graveyard_behaviour import GraveyardBehaviour
from tiles.door import Door


class Tile:
    tile_name: str
    tile_type: TileType
    tile_behaviour: TileBehaviour
    tile_doors: [Door]

    def __init__(self, tile_type: TileType):
        self.tile_type = tile_type
        match tile_type:
            case TileType.Foyer:
                self.tile_name = "Foyer"
                self.tile_behaviour = DefaultBehaviour()
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
