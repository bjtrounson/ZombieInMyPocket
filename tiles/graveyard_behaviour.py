from tiles.abstract_tile_behaviour import TileBehaviour


class GraveyardBehaviour(TileBehaviour):

    def action(self) -> str:
        return "Resolve a new card to bury totem"
