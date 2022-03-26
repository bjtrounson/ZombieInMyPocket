import cmd
from pprint import pprint
from cards.card_manager import CardManager
from game import Game
from level.level import Level
from parser import Parser
from pickle_manager import PickleManager, NoFileNameError
from player import Player
from tiles.tile import Tile
from tiles.tile_type import TileType


class Main(cmd.Cmd):
    _game: Game
    _player: Player
    _card_manager: CardManager
    _pickle_manager: PickleManager

    def __init__(self):
        super().__init__()
        self.aliases = {'quit': self.do_quit,
                        'help': self.do_help,
                        'rename': self.do_rename,
                        'stats': self.do_stats,
                        'health': self.do_player_health,
                        'attack': self.do_player_attack,
                        'save': self.do_save_game,
                        'load': self.do_load_game
                        }
        parser = Parser()

        self._player = Player(parser.args.health, parser.args.damage, [], 0, 0)
        level = Level([Tile(TileType.Foyer, 0, 0)], self._player)

        self._card_manager = CardManager()
        self._card_manager.add_all_cards()

        self._game = Game(9, level, self._card_manager.get_deck())
        self._pickle_manager = PickleManager()

        print(self._game._level.get_tile_player_is_on().get_tile_sides())
        print(self._card_manager.get_deck())
        pprint(vars(self._card_manager.get_deck()[0]))

    def do_help(self, args):
        """Show commands."""
        if args in self.aliases:
            args = self.aliases[args].__name__[3:]
            cmd.Cmd.do_help(self, args)
        else:
            print("Documented commands (type help <topic>):\n========================================")
            for key in self.aliases.keys():
                print(key)
            print("========================================")

    def do_quit(self, args):
        """Exit the program."""
        return True

    def do_player_health(self, args):
        """Show player health"""
        print(f"Health: {self._player.get_health()}")

    def do_player_attack(self, args):
        """Show player attack damage"""
        print(f"Attack: {self._player.get_attack_score()}")

    def do_stats(self):
        """Show player stats"""
        print(f"Health: {self._player.get_health()}\nAttack: {self._player.get_attack_score()}")

    def do_rename(self, args):
        """Rebind commands"""
        if len(args.split()) > 0:
            command = args.split()[0]
        else:
            command = input("Command to rename: ")

        # if "do_{}".format(cmd) in dir(Main):
        if command in self.aliases:
            if len(args.split()) > 1:
                new_cmd = args.split()[1]
            else:
                new_cmd = input("New command name: ")
            if new_cmd.isspace():
                raise TypeError("Blank response")
            self.aliases[new_cmd] = self.aliases[command]
            del self.aliases[command]
            # self.cmd.__name__ = "do_{}".format(new_cmd)
            print(f"Successfully changed {command} to {new_cmd}")
        else:
            print(f"--- Unknown command: {command}")

    def do_save_game(self, file_name: str) -> None:
        """
        save_game [file_name]
        Saves the current Game state
        """
        try:
            self._pickle_manager.serialize_object_to_file(file_name, self._game)
        except NoFileNameError:
            print("You need a file name!! 'save_game [file_name] Try Again'")

    def do_load_game(self, file_name: str) -> None:
        """
        load_game [file_name]
        Loads Game state from a file and makes it the current game
        """
        try:
            self._game = self._pickle_manager.deserialize_file_to_object(file_name)
        except NoFileNameError:
            print("You need a file name!! 'load_game [file_name] Try Again")

    def default(self, line):
        command, args, line = self.parseline(line)
        if command in self.aliases:
            return self.aliases[command](args)
        else:
            print(f"--- Unknown command: {line}")


if __name__ == '__main__':
    Main.prompt = 'ZombieInMyPocket$ '
    Main().cmdloop()
