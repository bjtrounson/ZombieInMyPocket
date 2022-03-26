import random

from cards.card import Card
from cards.card_manager import CardManager
from level.level import Level, NoDoorNearError, TileExistsError
from player import Player
from tiles.door import Door
from tiles.tile import Tile, RotationDirection
from tiles.tile_positions import TilePosition
from tiles.tile_type import TileType


class Game:
    _time: int
    _inside_tiles: list[Tile]
    _outside_tiles: list[Tile]
    _dev_cards: list[Card]
    _current_dev_cards: list[Card]
    _current_dev_card: Card | None
    _level: Level

    def __init__(self, time: int, level: Level, dev_cards: list[Card]):
        self._time = time
        self._level = level
        self._dev_cards = dev_cards
        self._current_dev_card = None
        self._inside_tiles = [Tile(TileType.Bedroom, 0, 0), Tile(TileType.DiningRoom, 0, 0),
                              Tile(TileType.EvilTemple, 0, 0), Tile(TileType.Storage, 0, 0),
                              Tile(TileType.Kitchen, 0, 0), Tile(TileType.Bathroom, 0, 0),
                              Tile(TileType.FamilyRoom, 0, 0)]
        self._outside_tiles = [Tile(TileType.Yard1, 0, 0), Tile(TileType.Yard2, 0, 0),
                               Tile(TileType.Yard3, 0, 0), Tile(TileType.Graveyard, 0, 0),
                               Tile(TileType.SittingArea, 0, 0), Tile(TileType.Garden, 0, 0),
                               Tile(TileType.Garage, 0, 0)]

    def setup(self):
        """

        :return:
        >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> card_manager  = CardManager()
        >>> card_manager.add_all_cards()
        >>> game = Game(9, level, card_manager.get_deck())
        >>> game.setup()
        """
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
        """
        Given a deck of cards or tiles, return deck in shuffled order
        :param deck: list[Card | Tile]
        :return : list[Card | Tile]
        >>> card_manager  = CardManager()
        >>> card_manager.add_all_cards()
        >>> cards = card_manager.get_deck()
        >>> Game.shuffle_decks(cards) #doctest: +ELLIPSIS
        [<cards.card.Card object at 0x...>]
        """
        return random.sample(deck, len(deck))

    def draw_tile(self) -> Tile:
        """
        Draws tile from inside or outside tiles
        :return: Tile
        >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> card_manager  = CardManager()
        >>> card_manager.add_all_cards()
        >>> game = Game(9, level, card_manager.get_deck())
        >>> game.draw_tile() #doctest: +ELLIPSIS
        <tiles.tile.Tile object at 0x...>
        """
        if self._level.get_player().get_is_inside():
            tile = self._inside_tiles[0]
            return tile
        else:
            tile = self._outside_tiles[0]
            return tile

    def move(self, entry_door: Door, exit_door: Door, new_tile: Tile):
        """

        :param entry_door: Door
        :param exit_door: Door
        :param new_tile: Tile
        :return:
        >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> card_manager  = CardManager()
        >>> card_manager.add_all_cards()
        >>> game = Game(9, level, card_manager.get_deck())
        >>> game.setup()
        >>> tile = game.draw_tile()
        >>> first_door = tiles[0].get_tile_sides()[0]
        >>> second_door = game.get_tile_doors(tile)[0]
        >>> game.move(first_door, second_door, tile)
        """
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
                self.tile_algorithm(new_tile)
            case TilePosition.East:
                new_tile = self.correct_tile_rotation(TilePosition.West, new_tile, exit_door)
                new_tile.set_pos(player_pos_x, player_pos_y + 1)
                self._level.get_player().set_player_pos(player_pos_x, player_pos_y + 1)
                new_tile.set_pos(player_pos_x, player_pos_y - 1)
                self.tile_algorithm(new_tile)
            case TilePosition.South:
                new_tile = self.correct_tile_rotation(TilePosition.North, new_tile, exit_door)
                new_tile.set_pos(player_pos_x, player_pos_y + 1)
                self._level.get_player().set_player_pos(player_pos_x, player_pos_y + 1)
                self.tile_algorithm(new_tile)
            case TilePosition.West:
                new_tile = self.correct_tile_rotation(TilePosition.East, new_tile, exit_door)
                new_tile.set_pos(player_pos_x, player_pos_y + 1)
                self._level.get_player().set_player_pos(player_pos_x, player_pos_y + 1)
                self.tile_algorithm(new_tile)

    @staticmethod
    def correct_tile_rotation(correct_door_position: TilePosition, new_tile: Tile, exit_door: Door) -> Tile:
        """
        Given a tile, tile position and an exit door on the tile, return the tile in the correct rotation
        :param correct_door_position: TilePosition
        :param new_tile: Tile
        :param exit_door: Door
        :return: Tile

        >>> tile = Tile(TileType.Foyer, 0, 0)
        >>> door_position = TilePosition.South
        >>> side = tile.get_side_from_index(tile.get_door_index_from_position(TilePosition.North.value))
        >>> door = Door(side.original_tile_side)
        >>> Game.correct_tile_rotation(door_position, tile, door) #doctest: +ELLIPSIS
        <tiles.tile.Tile object at 0x...>
        """
        exit_door_position_on_tile: int = new_tile.get_tile_sides().index(exit_door)
        while exit_door_position_on_tile != correct_door_position.value:
            new_tile.rotate_tile(RotationDirection.Right)
            exit_door_position_on_tile = new_tile.get_tile_sides().index(exit_door)
        return new_tile

    @staticmethod
    def get_tile_doors(tile: Tile) -> list[Door]:
        """

        :param tile: Tile
        :return: list[Door]
        >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> card_manager  = CardManager()
        >>> card_manager.add_all_cards()
        >>> game = Game(9, level, card_manager.get_deck())
        >>> game.get_tile_doors(game.draw_tile()) #doctest: +ELLIPSIS
        [<tiles.door.Door object at 0x...>]
        """
        doors_list: list[Door] = []
        for side in tile.get_tile_sides():
            if type(side) is Door:
                doors_list.append(side)
        return doors_list

    def tile_algorithm(self, new_tile: Tile) -> bool:
        """
        Give a tile to be added to the level
        :param new_tile: Tile
        :return: bool
        >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> card_manager = CardManager()
        >>> card_manager.add_all_cards()
        >>> game = Game(9, level, card_manager.get_deck())
        >>> tile = game.draw_tile()
        >>> tile.set_pos(0, 1)
        >>> game.tile_algorithm(tile)
        True
        """
        try:
            if self._level.get_player().get_is_inside():
                self._level.add_new_tile(new_tile)
                self._inside_tiles.pop(self._get_index_of_tile(new_tile))
                return True
            else:
                self._level.add_new_tile(new_tile)
                self._outside_tiles.pop(self._get_index_of_tile(new_tile))
                return True
        except TileExistsError:
            print("Tile already exists there!")
            return False
        except NoDoorNearError:
            print("No Doors exist there!")
            return False

    def _get_index_of_tile(self, target_tile: Tile) -> int:
        """
        Given tile, return tile index
        :param target_tile:
        :return int:
        >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> card_manager  = CardManager()
        >>> card_manager.add_all_cards()
        >>> game = Game(9, level, card_manager.get_deck())
        >>> tile = game.draw_tile()
        >>> game._get_index_of_tile(tile)
        0
        """
        if self._level.get_player().get_is_inside():
            return self._inside_tiles.index(target_tile)
        else:
            return self._outside_tiles.index(target_tile)

    def pickup_item(self):
        pass

    def attack(self, zombie_count: int, attack_score: int):
        """

        :param zombie_count: int
        :param attack_score: int
        :return:
        >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> card_manager  = CardManager()
        >>> card_manager.add_all_cards()
        >>> game = Game(9, level, card_manager.get_deck())
        >>> game.attack(4, 6)
        """
        if zombie_count <= attack_score:
            return
        else:
            damage_taken = zombie_count - attack_score
            self._level.get_player().set_health(self._level.get_player().get_health() - damage_taken)

    def cower(self) -> None:
        """

        :return:
         >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> card_manager  = CardManager()
        >>> card_manager.add_all_cards()
        >>> game = Game(9, level, card_manager.get_deck())
        >>> game.cower()
        """
        self._level.get_player().set_health(self._level.get_player().get_health() + 3)
