from tiles.abstract_tile_behaviour import TileBehaviour


class StorageBehaviour(TileBehaviour):

    def action(self) -> str:
        return "May Draw a new card to find an item"
