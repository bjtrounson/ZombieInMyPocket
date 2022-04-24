import cmd
import os

from cards.card_manager import CardManager
from file_manager.file_manager import FileManager
from game import Game
from game_options import GameOptions
from level.level import Level
from parser import Parser
from pickle_manager.pickle_manager import PickleManager
from player import Player
from tiles.tile import Tile
from tiles.tile_type import TileType


class Commands(cmd.Cmd):
    _game: Game
    _card_manager: CardManager
    _pickle_manager: PickleManager
    _file_manager: FileManager
    _game_options: GameOptions

    def __init__(self):
        super().__init__()
        cwd: str = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        parser = Parser()
        try:
            parser.add_args()
            self._game_options = GameOptions(parser.args.health, parser.args.damage, parser.args.item_limit,
                                             parser.args.start_time, parser.args.end_time)
        except ValueError as e:
            print(e)
            print("Applying defaults")
            self._game_options = GameOptions(6, 1, 2, 9, 11)
        player: Player = Player(self._game_options.player_health, self._game_options.player_damage,
                                self._game_options.player_item_limit, [], 0, 0)
        tiles: list[Tile] = [Tile(TileType.Foyer, 0, 0)]
        level = Level(tiles, player)
        self._game = Game(self._game_options.game_start_time, self._game_options.game_end_time, level)
        self._pickle_manager = PickleManager(cwd)
        self._file_manager = FileManager(cwd)

    def preloop(self) -> None:
        intro: str = self._file_manager.extract_intro_text()
        print(intro)
        super(Commands, self).preloop()

    def do_game_info(self, args) -> None:
        print(f"Current Tile: {self._game.get_current_tile().tile_name}")
        print(f"Player Health: {self._game.get_player_from_level().get_health()}")
        print(f"Player Attack: {self._game.get_player_from_level().get_attack_score()}")
        print(f"Player Items: {[item.item_name for item in self._game.get_player_from_level().get_items()]}")
        print(f"Player Position X: {self._game.get_player_from_level().get_x()} "
              f"Y: {self._game.get_player_from_level().get_y()}")

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def help_game_info(self):
        print('\n'.join(['game_info', 'Shows current game information in format below',
                         'Current Tile: [Tile Name]',
                         'Player Health: [Health]',
                         'Player Attack: [Attack Score]',
                         'Player Items: [Items]',
                         'Player Position X: [X Cord], Y: [Y Cord]',
                         ]))

    def do_next_turn(self, args) -> None:
        next_tile = self._game.draw_tile()
        current_tile = self._game.get_current_tile()
        entry_door = None
        while entry_door is None:
            try:
                entry_door = self._game.get_door_from_input(next_tile, True)
            except ValueError as e:
                print(e)
        exit_door = None
        while exit_door is None:
            try:
                exit_door = self._game.get_door_from_input(current_tile, False)
            except ValueError as e:
                print(e)
        self._game.move(entry_door, exit_door, next_tile)
        self._game.draw_dev_card()
        self._game.activate_time_action(self._game.get_current_dev_card())

        if self._game.get_player_from_level().get_health() <= 0:
            print("Game Over! You Died")

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def help_next_turn(self):
        print('\n'.join(['next_turn', 'Starts the a turn in the game.',
                         'You will be asked for the door you want to enter on the new tile then,',
                         'You will be asked the door you want to exit on the current tile.',
                         'You then move to that tile and a dev card is draw and the action is played out',
                         'If you happen to die from zombies the game will end.']))

    def do_cower(self, args) -> None:
        self._game.cower()

    def help_cower(self):
        print('\n'.join(['cower', 'Cower to regain 3 health points']))

    def do_save_game_options(self, file_name: str) -> None:
        self._file_manager.serialize_game_options_to_json(file_name, self._game_options)

    def help_save_game_options(self):
        print('\n'.join(['save_game_options [file_name]', 'Saves the game options used to a json file']))

    def do_load_game_options(self, file_name: str) -> None:
        try:
            game_options = self._file_manager.deserialize_json_to_game_options(file_name)
            self._game.get_player_from_level().set_health(game_options.player_health)
            self._game.get_player_from_level().set_attack_score(game_options.player_damage)
            self._game.get_player_from_level().set_item_limit(game_options.player_item_limit)
            self._game.set_game_start_time(game_options.game_start_time)
            self._game.set_game_end_time(game_options.game_end_time)
        except Exception as e:
            print(e)

    def help_load_game_options(self):
        print('\n'.join(['load_game_options [file_name]', 'Loads game options from a json file']))

    def do_save_game(self, file_name: str) -> None:
        self._pickle_manager.serialize_object_to_file(file_name, self._game)

    def help_save_game(self):
        print('\n'.join(['save_game [file_name]', 'Saves the current game to a file']))

    def do_load_game(self, file_name: str) -> None:
        self._game = self._pickle_manager.deserialize_file_to_object(file_name)

    def help_load_game(self):
        print('\n'.join(['load_game [file_name]',
                         'Loads a previously saved game from a file and runs it as the current game']))

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def do_EOF(self, line):
        """Exit Program"""
        return True
