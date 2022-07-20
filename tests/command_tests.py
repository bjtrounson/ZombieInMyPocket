import os
import sys
import unittest
from unittest.mock import call

from interpreter import Interpreter
from mock import patch

from pickle_manager.pickle_manager import PickleManager


class CommandsTestCases(unittest.TestCase):
    def setUp(self) -> None:
        self.current_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.pickle_manager = PickleManager(self.current_dir)

    @patch('builtins.print')
    def test_when_help_commands(self, mock_print):
        self.interpreter = Interpreter()
        self.interpreter.help_cower()
        mock_print.assert_called_with('cower\nCower to regain 3 health points')
        self.interpreter.help_next_turn()
        mock_print.assert_called_with(('next_turn\nStarts the a turn in the game.\n'
                                       'You will be asked for the door you want to enter on the new tile then,\n'
                                       'You will be asked the door you want to exit on the current tile.\n'
                                       'You then move to that tile and a dev card is draw and the action is played'
                                       ' out\n'
                                       'If you happen to die from zombies the game will end.'))
        self.interpreter.help_game_info()
        mock_print.assert_called_with(("game_info\nShows current game information in format below\n"
                                       "Current Tile: [Tile Name]\n"
                                       "Player Health: [Health]\n"
                                       "Player Attack: [Attack Score]\n"
                                       "Player Items: [Items]\n"
                                       "Player Position X: [X Cord], Y: [Y Cord]"))
        self.interpreter.help_load_game()
        mock_print.assert_called_with(("load_game [file_name]\nLoads a previously saved game from a file and runs it "
                                       "as the current game"))
        self.interpreter.help_save_game()
        mock_print.assert_called_with('save_game [file_name]\nSaves the current game to a file')
        self.interpreter.help_load_game_options()
        mock_print.assert_called_with('load_game_options [file_name]\nLoads game options from a json file')
        self.interpreter.help_save_game_options()
        mock_print.assert_called_with('save_game_options [file_name]\nSaves the game options used to a json file')

    @patch('builtins.print')
    def test_game_commands_output(self, mock_print):
        self.interpreter = Interpreter()
        self.interpreter.do_cower(None)
        self.assertEqual(self.interpreter._game.get_player_from_level().get_health(), 9)
        self.interpreter.do_game_info(None)
        mock_print.assert_called_with("Player Position X: 0 Y: 0")

    @patch('builtins.input', create=True)
    def test_game_commands_input(self, mock_input):
        self.interpreter = Interpreter()
        mock_input.side_effect = ['1', '1', 'No', 'attack']
        self.interpreter.do_next_turn(None)
        self.assertNotEqual({self.interpreter._game.get_player_from_level().get_x(),
                             self.interpreter._game.get_player_from_level().get_y()}, {0, 0})

    @patch('builtins.input', create=True)
    def test_when_do_next_turn_entry_door_input_index_error(self, mock_input):
        raised = False
        try:
            self.interpreter = Interpreter()
            mock_input.side_effect = ['6', '1', 'No', 'attack']
            self.interpreter.do_next_turn(None)
        except IndexError:
            raised = True
        self.assertTrue(raised)

    @patch('builtins.input', create=True)
    def test_when_do_next_turn_exit_door_input_index_error(self, mock_input):
        raised = False
        try:
            self.interpreter = Interpreter()
            mock_input.side_effect = ['1', '7', 'No', 'attack']
            self.interpreter.do_next_turn(None)
        except IndexError:
            raised = True
        self.assertTrue(raised)

    @patch('builtins.print')
    @patch('builtins.input', create=True)
    def test_when_do_next_turn_entry_door_input_value_error(self, mock_input, mock_print):
        self.interpreter = Interpreter()
        mock_input.side_effect = ['hello', '1', '1', 'No', 'attack']
        self.interpreter.do_next_turn(None)
        self.assertNotEqual({self.interpreter._game.get_player_from_level().get_x(),
                             self.interpreter._game.get_player_from_level().get_y()}, {0, 0})

    @patch('builtins.print')
    @patch('builtins.input', create=True)
    def test_when_do_next_turn_exit_door_input_value_error(self, mock_input, mock_print):
        self.interpreter = Interpreter()
        mock_input.side_effect = ['1', 'hello', '1', 'No', 'attack']
        self.interpreter.do_next_turn(None)
        self.assertNotEqual({self.interpreter._game.get_player_from_level().get_x(),
                             self.interpreter._game.get_player_from_level().get_y()}, {0, 0})

    @patch('builtins.print')
    @patch('builtins.input', create=True)
    def test_when_do_next_turn_player_health_zero(self, mock_input, mock_print):
        self.interpreter = Interpreter()
        self.interpreter._game.get_player_from_level().set_health(-1)
        mock_input.side_effect = ['1', '1', 'No', 'attack']
        self.interpreter.do_next_turn(None)
        mock_print.assert_called_with("Game Over! You Died")

    @patch('builtins.print')
    def test_when_do_load_game_options_command_exception(self, mock_print):
        self.interpreter = Interpreter()
        self.interpreter.do_load_game_options("hello")
        self.assertEqual(call("File not found 'hello'", "FileNotFoundError(2, 'No such file or directory')"),
                         mock_print.mock_calls[0])

    def test_when_do_save_game_options_command(self):
        self.interpreter = Interpreter()
        self.interpreter._game_options.player_health = 9
        if os.path.exists(os.path.join(self.current_dir, f'testing.json')):
            self.pickle_manager.remove_save("testing")
        self.interpreter.do_save_game_options("testing")
        expected = False
        actual = os.path.isfile(os.path.join(self.current_dir, f'testing.json'))
        self.assertEqual(expected, actual)

    def test_when_do_load_game_options_command(self):
        self.interpreter = Interpreter()
        self.interpreter.do_load_game_options("testing")
        expected = 9
        actual = self.interpreter._game.get_player_from_level().get_health()
        self.assertEqual(expected, actual)

    @patch('builtins.input', create=True)
    def test_when_do_save_game_command(self, mock_input):
        self.interpreter = Interpreter()
        mock_input.side_effect = ['1', '1', 'No', 'attack']
        self.interpreter.do_next_turn(None)
        if os.path.exists(os.path.join(self.current_dir, 'testing-game.pkl')):
            self.pickle_manager.remove_save("testing-game")
        self.interpreter.do_save_game("testing-game")
        expected = False
        actual = os.path.isfile(os.path.join(self.current_dir, 'testing-game.pkl'))
        self.assertEqual(expected, actual)

    def test_when_do_load_game_command(self):
        self.interpreter = Interpreter()
        self.interpreter.do_load_game("testing-game")
        self.assertNotEqual({self.interpreter._game.get_player_from_level().get_x(),
                             self.interpreter._game.get_player_from_level().get_y()}, {0, 0})

    def test_when_do_EOF_command(self):
        self.interpreter = Interpreter()
        self.assertTrue(self.interpreter.do_EOF(None))

    @patch('builtins.print')
    def test_when_preloop_command(self, mock_print):
        self.interpreter = Interpreter()
        self.interpreter.preloop()
        mock_print.assert_called_with("Welcome to Zombie In My Pocket, The dead walk the earth. You must search the "
                                      "house for the Evil\n"
                                      "Temple, and find the zombie totem. Then take the totem outside, and bury it in "
                                      "the Graveyard,\n"
                                      "all before the clock strikes midnight.")

    def test_when_instantiate_commands_constructor(self):
        sys.argv.append('-hp=0')
        interpreter = Interpreter()
        self.assertEqual(6, interpreter._game.get_player_from_level().get_health())


if __name__ == '__main__':
    unittest.main()
