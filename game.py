import random

from level.level import Level, NoDoorNearError, TileExistsError
from player import Player
from tiles.door import Door
from tiles.tile import Tile, RotationDirection
from tiles.tile_type import TileType
from cards.card import Card
from tiles.tile_positions import TilePosition


class Game:
    _time: int
    _inside_tiles: list[Tile]
    _outside_tiles: list[Tile]
    _dev_cards: list[Card]
    _current_dev_cards: list[Card]
    _current_dev_card: Card
    _level: Level

    def __init__(self, time: int, level: Level, dev_cards: list[Card]):
        self._time = time
        self._level = level
        self._dev_cards = dev_cards
        self._inside_tiles = [Tile(TileType.Bedroom, 0, 0), Tile(TileType.DiningRoom, 0, 0),
                              Tile(TileType.EvilTemple, 0, 0), Tile(TileType.Storage, 0, 0),
                              Tile(TileType.Kitchen, 0, 0), Tile(TileType.Bathroom, 0, 0),
                              Tile(TileType.FamilyRoom, 0, 0)]
        self._outside_tiles = [Tile(TileType.Yard1, 0, 0), Tile(TileType.Yard2, 0, 0),
                               Tile(TileType.Yard3, 0, 0), Tile(TileType.Graveyard, 0, 0),
                               Tile(TileType.SittingArea, 0, 0), Tile(TileType.Garden, 0, 0),
                               Tile(TileType.Garage, 0, 0)]

    def setup(self):
        # Shuffle and setup development cards
        self.shuffle_decks(self._dev_cards)
        del self._dev_cards[2:]
        self._current_dev_card = self._dev_cards[0]
        self._dev_cards.pop(0)
        # Shuffle Inside Tiles
        self.shuffle_decks(self._inside_tiles)
        # Shuffle Outside Tiles
        self.shuffle_decks(self._outside_tiles)

    @staticmethod
    def shuffle_decks(deck: list[Card | Tile]) -> list[Card | Tile]:
        random.shuffle(deck)
        return deck

    def draw_tile(self) -> Tile:
        if self._level.get_player().get_is_inside():
            tile = self._inside_tiles[0]
            return tile
        else:
            tile = self._outside_tiles[0]
            return tile

    def move(self, entry_door: Door, exit_door: Door, new_tile: Tile):
        player_pos_x = self._level.get_player().get_x()
        player_pos_y = self._level.get_player().get_y()

        # Gets the position of the door on the current tile
        entry_door_position_on_tile: int = self._level.get_tile_player_is_on().get_tile_sides().index(entry_door)

        match entry_door_position_on_tile:
            case TilePosition.North:
                if self._level.get_tile_player_is_on().tile_type == TileType.DiningRoom:
                    new_tile = Tile(TileType.Patio, 0, 0)
                new_tile = self.correct_tile_rotation(TilePosition.South, new_tile, exit_door)
                new_tile.set_pos(player_pos_x, player_pos_y + 1)
                self._level.get_player().set_player_pos(player_pos_x, player_pos_y + 1)
                self.movement_algorithm(new_tile)
            case TilePosition.East:
                new_tile = self.correct_tile_rotation(TilePosition.West, new_tile, exit_door)
                new_tile.set_pos(player_pos_x, player_pos_y + 1)
                self._level.get_player().set_player_pos(player_pos_x, player_pos_y + 1)
                new_tile.set_pos(player_pos_x, player_pos_y - 1)
                self.movement_algorithm(new_tile)
            case TilePosition.South:
                new_tile = self.correct_tile_rotation(TilePosition.North, new_tile, exit_door)
                new_tile.set_pos(player_pos_x, player_pos_y + 1)
                self._level.get_player().set_player_pos(player_pos_x, player_pos_y + 1)
                self.movement_algorithm(new_tile)
            case TilePosition.West:
                new_tile = self.correct_tile_rotation(TilePosition.East, new_tile, exit_door)
                new_tile.set_pos(player_pos_x, player_pos_y + 1)
                self._level.get_player().set_player_pos(player_pos_x, player_pos_y + 1)
                self.movement_algorithm(new_tile)

    @staticmethod
    def correct_tile_rotation(correct_door_position: TilePosition, new_tile: Tile, exit_door: Door) -> Tile:
        exit_door_position_on_tile: int = new_tile.get_tile_sides().index(exit_door)
        while exit_door_position_on_tile != correct_door_position:
            new_tile.rotate_tile(RotationDirection.Right)
            exit_door_position_on_tile = new_tile.get_tile_sides().index(exit_door)
        return new_tile

    @staticmethod
    def get_tile_sides(tile: Tile) -> list[Door]:
        doors_list: list[Door] = []
        for side in tile.get_tile_sides():
            if type(side) is Door:
                doors_list.append(side)
        return doors_list

    def movement_algorithm(self, new_tile: Tile):
        try:
            if self._level.get_player().get_is_inside():
                self._level.add_new_tile(new_tile)
                self._inside_tiles.pop(self._get_index_of_tile(new_tile))
            else:
                self._level.add_new_tile(new_tile)
                self._outside_tiles.pop(self._get_index_of_tile(new_tile))
        except TileExistsError:
            print("Tile already exists there!")
        except NoDoorNearError:
            print("No Doors exist there!")

    def _get_index_of_tile(self, target_tile: Tile) -> int:
        if self._level.get_player().get_is_inside():
            return self._inside_tiles.index(target_tile)
        else:
            return self._outside_tiles.index(target_tile)

    def pickup_item(self):
        pass

    def attack(self, zombie_count: int, attack_score: int):
        if zombie_count < attack_score:
            return
        else:
            damage_taken = zombie_count - attack_score
            self._level.get_player().set_health(self._level.get_player().get_health() - damage_taken)

    def cower(self) -> None:
        self._level.get_player().set_health(self._level.get_player().get_health() + 3)
