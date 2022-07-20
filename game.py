import random

from cards.abstract_time_behaviour import AbstractTimeBehaviour
from cards.bad_time_behaviour import BadTimeBehaviour
from cards.card import Card
from cards.card_manager import CardManager
from items.item import Item
from level.level import Level, NoDoorNearError, TileExistsError
from player import Player
from tiles.door import Door
from tiles.tile import Tile, RotationDirection
from tiles.tile_manager import TileManager
from tiles.tile_positions import TilePosition
from tiles.tile_type import TileType


class ZombieDoorException(Exception):
    pass


class Game:
    _time: int
    _end_time: int
    _inside_tiles: list[Tile]
    _outside_tiles: list[Tile]
    _dev_cards: list[Card]
    _current_dev_card: Card | None
    _card_manager: CardManager
    _tile_manager: TileManager
    _level: Level

    def __init__(self, start_time: int, end_time: int, level: Level):
        self._time = start_time
        self._end_time = end_time
        self._level = level
        self._card_manager = CardManager()
        self._tile_manager = TileManager()
        self._current_dev_card = None
        self._dev_cards = []
        self._card_manager.add_all_cards()
        self._tile_manager.add_inner_tiles()
        self._tile_manager.add_outer_tiles()
        self._inside_tiles = self._tile_manager.get_inner_tile_deck()
        self._outside_tiles = self._tile_manager.get_outer_tile_deck()
        self.setup()

    def setup(self):
        """

        :return:
        >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> game = Game(9, level)
        >>> game.setup()
        """
        # Shuffle and setup development cards
        self.setup_dev_cards()
        # Shuffle Inside Tiles
        self._inside_tiles = self.shuffle_decks(self._inside_tiles)
        # Shuffle Outside Tiles
        self._outside_tiles = self.shuffle_decks(self._outside_tiles)

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
        >>> game = Game(9, level)
        >>> game.draw_tile() #doctest: +ELLIPSIS
        <tiles.tile.Tile object at 0x...>
        """
        if self._level.get_player().get_is_inside():
            tile = self._inside_tiles[0]
            return tile
        else:
            tile = self._outside_tiles[0]
            return tile

    def setup_dev_cards(self):
        self._dev_cards = self._card_manager.get_deck()
        self._dev_cards = self.shuffle_decks(self._dev_cards)
        del self._dev_cards[2:]
        self._current_dev_card = self._dev_cards[0]
        self._dev_cards.pop(0)

    def draw_dev_card(self):
        if len(self._dev_cards) <= 0:
            self.setup_dev_cards()
            self._time = self._time + 1
        else:
            self._current_dev_card = self._dev_cards[0]
            self._dev_cards.pop(0)

    def move(self, entry_door: Door, exit_door: Door, new_tile: Tile):
        """

        :param entry_door: Door
        :param exit_door: Door
        :param new_tile: Tile
        :return:
        >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> game = Game(9, 11, level)
        >>> game.setup()
        >>> tile = game.draw_tile()
        >>> first_door = tiles[0].get_tile_sides()[0]
        >>> second_door = game.get_tile_doors(tile)[0]
        >>> game.move(first_door, second_door, tile)
        """
        player_pos_x = self._level.get_player().get_x()
        player_pos_y = self._level.get_player().get_y()

        # Gets the position of the door on the current tile
        exit_door_position_on_tile: TilePosition = TilePosition(self._level.get_tile_player_is_on().
                                                                get_tile_sides().index(exit_door))
        match exit_door_position_on_tile:
            case TilePosition.North:
                new_tile = self.correct_tile_rotation(TilePosition.South, new_tile, entry_door)
                self.movement_algorithm(player_pos_x, player_pos_y + 1, new_tile, exit_door)
            case TilePosition.East:
                new_tile = self.correct_tile_rotation(TilePosition.West, new_tile, entry_door)
                self.movement_algorithm(player_pos_x + 1, player_pos_y, new_tile, exit_door)
            case TilePosition.South:
                new_tile = self.correct_tile_rotation(TilePosition.North, new_tile, entry_door)
                self.movement_algorithm(player_pos_x, player_pos_y - 1, new_tile, exit_door)
                new_tile.set_pos(player_pos_x, player_pos_y - 1)
            case TilePosition.West:
                new_tile = self.correct_tile_rotation(TilePosition.East, new_tile, entry_door)
                self.movement_algorithm(player_pos_x - 1, player_pos_y, new_tile, exit_door)

    def movement_algorithm(self, player_pos_x: float, player_pos_y: float, new_tile: Tile, exit_door: Door):
        new_tile.set_pos(player_pos_x, player_pos_y)
        try:
            if self.tile_algorithm(new_tile):
                self._level.get_player().set_player_pos(player_pos_x, player_pos_y)
            else:
                if len(self._level.get_available_doors(new_tile)) == 0:
                    raise ZombieDoorException("No Doors Available")
                else:
                    raise Exception("Unable to move there")
        except ZombieDoorException as e:
            if self._level.get_available_doors(new_tile) is None:
                self.create_zombie_door(new_tile, exit_door)
                print("Zombie Door Created")
                zombie_door_behaviour = BadTimeBehaviour(3, "3 Zombies")
                self._bad_time_behaviour(zombie_door_behaviour)
            else:
                print(e)
        except Exception as e:
            print(e)

    def create_zombie_door(self, tile: Tile, exit_door: Door):
        available_walls = self._level.get_walls_on_tile(tile)
        available_walls_input = None
        while available_walls_input is None:
            try:
                for wall_num in range(len(available_walls)):
                    print(f"Wall {wall_num + 1}: "
                          f"{TilePosition(tile.get_tile_sides().index(tile.get_side_from_index(wall_num))).name}")
                option_input = input("What wall do you want to added a zombie door too? e.g. 1-3 ")
                if isinstance(option_input, int):
                    door = Door(tile.get_side_from_index(option_input - 1).get_tile_side())
                    tile.get_tile_sides()[option_input - 1] = door
                    self.move(door, exit_door, tile)
                available_walls_input = True
            except ValueError:
                print("Not a number please put a number from 1-3")
            except IndexError:
                print("That value is out of range")

    @staticmethod
    def correct_tile_rotation(correct_door_position: TilePosition, new_tile: Tile, entry_door: Door) -> Tile:
        """
        Given a tile, tile position and an exit door on the tile, return the tile in the correct rotation
        :param correct_door_position: TilePosition
        :param new_tile: Tile
        :param entry_door: Door
        :return: Tile

        >>> tile = Tile(TileType.Foyer, 0, 0)
        >>> door_position = TilePosition.South
        >>> side = tile.get_side_from_index(tile.get_door_index_from_position(TilePosition.North.value))
        >>> door = Door(side.original_tile_side)
        >>> Game.correct_tile_rotation(door_position, tile, door) #doctest: +ELLIPSIS
        <tiles.tile.Tile object at 0x...>
        """
        entry_door_position_on_tile: int = new_tile.get_tile_sides().index(entry_door)
        while entry_door_position_on_tile != correct_door_position.value:
            new_tile.rotate_tile(RotationDirection.Right)
            entry_door_position_on_tile = new_tile.get_tile_sides().index(entry_door)
        return new_tile

    @staticmethod
    def get_tile_doors(tile: Tile) -> list[Door]:
        """

        :param tile: Tile
        :return: list[Door]
        >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> game = Game(9, 11, level)
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
        >>> game = Game(9, 11, level)
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
        >>> game = Game(9, 11, level)
        >>> tile = game.draw_tile()
        >>> game._get_index_of_tile(tile)
        0
        """
        if self._level.get_player().get_is_inside():
            return self._inside_tiles.index(target_tile)
        else:
            return self._outside_tiles.index(target_tile)

    def pickup_item(self, item: Item):
        pickup_input = None
        while pickup_input is None:
            try:
                option_input = input("Do you want to pick up the item? e.g. Yes or No -> ").lower()
                if option_input == "yes" or option_input == "no":
                    if option_input == "yes":
                        try:
                            self._level.get_player().add_item(item)
                        except ValueError:
                            print("Unable to add item because inventory is full")
                    pickup_input = True
                else:
                    raise ValueError
            except ValueError:
                print("Incorrect input please put Yes or No")

    def replace_item(self, item: Item):
        replace_item_input = None
        while replace_item_input is None:
            try:
                option_input = input(f"Do you want to replace a item in your inventory with {item.item_name}?").lower()
                if option_input == "yes" or option_input == "no":
                    if option_input == "yes":
                        try:
                            item_to_replace = self.available_replaceable_items()
                            self._level.get_player().replace_item(item_to_replace, item)
                            print("Item Replaced")
                        except ValueError:
                            print("Unable to add item because inventory is full")
                    replace_item_input = True
                else:
                    raise ValueError
            except ValueError:
                print("Incorrect input please put Yes or No")

    def available_replaceable_items(self) -> Item:
        available_items_input = None
        while available_items_input is None:
            try:
                for i in range(len(self._level.get_player().get_items())):
                    print(f"Item {i + 1}: {self._level.get_player().get_items()[i].item_name}")
                item_choice = input("What item do you want to replace? 1-4")
                if isinstance(item_choice, int):
                    item = self._level.get_player().get_items()[item_choice - 1]
                    return item
                else:
                    raise ValueError
            except ValueError:
                print("Not a number please input a number")
            except IndexError:
                print("That value is out of range")

    def attack(self, zombie_count: int, attack_score: int):
        """
        :param zombie_count: int
        :param attack_score: int
        :return:
        >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> game = Game(9, 11, level)
        >>> game.attack(4, 6)
        """
        if zombie_count <= attack_score:
            print("You took no damage :)")
            return
        else:
            damage_taken = zombie_count - attack_score
            self._level.get_player().set_health(self._level.get_player().get_health() - damage_taken)
            print(f"You took {self._level.get_player().get_health() - damage_taken} damage!")

    def cower(self) -> None:
        """

        :return:
         >>> player = Player(6, 1, [], 0, 0)
        >>> tiles = [Tile(TileType.Foyer, 0, 0)]
        >>> level = Level(tiles, player)
        >>> game = Game(9, level)
        >>> game.cower()
        """
        self._level.get_player().set_health(self._level.get_player().get_health() + 3)

    def activate_time_action(self, card: Card):
        time_action = card.get_time_action(self._time)
        time_action_name = type(time_action.time_behaviour).__name__
        match time_action_name:
            case "NeutralTimeBehaviour":
                print(time_action.time_behaviour.action())
            case "BadTimeBehaviour":
                self._bad_time_behaviour(time_action.time_behaviour)
            case "PassiveBadTimeBehaviour":
                self._level.get_player(). \
                    set_health(self._level.get_player().get_health() - time_action.time_behaviour.action())
            case "GoodTimeBehaviour":
                print(time_action.time_behaviour.message)
                self._level.get_player(). \
                    set_health(self._level.get_player().get_health() + time_action.time_behaviour.action())
            case "ItemTimeBehaviour":
                item: Item = time_action.time_behaviour.action()
                print(f"{time_action.time_behaviour.message}: {item.item_name}")
                self.pickup_item(item)

    def _bad_time_behaviour(self, time_behaviour: AbstractTimeBehaviour):
        action_done = None
        print(time_behaviour.message)
        while action_done is None:
            try:
                option_input = input("Do you want to attack or run?").lower()
                if option_input == "attack" or option_input == "run":
                    if option_input == "attack":
                        self.attack(time_behaviour.action(),
                                    self._level.get_player().get_attack_score())
                    elif option_input == "run":
                        self.runaway()
                    action_done = True
                else:
                    raise ValueError
            except ValueError as e:
                print(e)

    def runaway(self):
        available_tiles = self.player_run_away_tiles_available()
        for tile_num in range(len(available_tiles)):
            print(f"Tile {tile_num + 1}: {available_tiles[tile_num].tile_name}")
        runaway_tile = None
        while runaway_tile is None:
            try:
                tile_index = self.runaway_tile_input()
                runaway_tile = available_tiles[tile_index]
            except ValueError as e:
                print(e)
        self._level.get_player().set_player_pos(runaway_tile.get_x(), runaway_tile.get_y())
        self._level.get_player().set_health(self._level.get_player().get_health() - 1)
        print("You took 1 damage from running away")

    @staticmethod
    def runaway_tile_input() -> int:
        door_input = int(input("Which tile do you want to run back to? e.g. 1-4"))
        if not isinstance(door_input, int):
            raise ValueError
        else:
            return door_input - 1

    def player_run_away_tiles_available(self) -> list[Tile]:
        player_tile = self._level.get_tile_player_is_on()
        current_tile_door_info = self._level.get_door_info_on_tile(player_tile)
        player_x = self._level.get_player().get_x()
        player_y = self._level.get_player().get_y()
        tile_list: list[Tile] = []
        for door_dict in current_tile_door_info:
            door_pos: TilePosition = door_dict.get("door_position")
            match door_pos:
                case TilePosition.North:
                    if self._level.check_if_tile_already_exists(player_x, player_y + 1):
                        tile: Tile = self._level.get_tile_by_cords(player_x, player_y + 1)
                        tile_list.append(tile)
                case TilePosition.East:
                    if self._level.check_if_tile_already_exists(player_x + 1, player_y):
                        tile: Tile = self._level.get_tile_by_cords(player_x + 1, player_y)
                        tile_list.append(tile)
                case TilePosition.West:
                    if self._level.check_if_tile_already_exists(player_x - 1, player_y):
                        tile: Tile = self._level.get_tile_by_cords(player_x - 1, player_y)
                        tile_list.append(tile)
                case TilePosition.South:
                    if self._level.check_if_tile_already_exists(player_x, player_y - 1):
                        tile: Tile = self._level.get_tile_by_cords(player_x, player_y - 1)
                        tile_list.append(tile)
        return tile_list

    def get_door_from_input(self, tile: Tile, new_tile: bool) -> Door:
        print(f"Next Tile: {tile.tile_name}" if new_tile else f"Current Tile: {tile.tile_name}")
        print("Entry Doors of Next Tile: " if new_tile else "Exit Doors of Current Tiles")
        for door_num in range(len(self._level.get_available_doors(tile))):
            print(f"Door {door_num + 1}: Facing {self._level.get_available_doors(tile)[door_num].get_tile_side().name}")
        door_input = int(input("What door do you want to enter from? e.g. 1-4"
                               if new_tile else "What door do you want to exit from? e.g. 1-4"))
        if not isinstance(door_input, int):
            raise ValueError
        else:
            return self.get_tile_doors(tile)[door_input - 1]

    def get_current_tile(self) -> Tile:
        return self._level.get_tile_player_is_on()

    def get_current_dev_card(self) -> Card:
        return self._current_dev_card

    def get_player_from_level(self):
        return self._level.get_player()

    def set_game_start_time(self, start_time: int):
        self._time = start_time

    def set_game_end_time(self, end_time: int):
        self._end_time = end_time
