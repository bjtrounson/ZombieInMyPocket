from commands.command import Command


class HelpCommands(Command):
    def __init__(self, cwd):
        super().__init__(cwd)

    def help_load_game(self):
        print('\n'.join(['load_game [file_name]',
                         'Loads a previously saved game from a file and runs it as the current game']))

    def help_save_game(self):
        print('\n'.join(['save_game [file_name]', 'Saves the current game to a file']))

    def help_load_game_options(self):
        print('\n'.join(['load_game_options [file_name]', 'Loads game options from a json file']))

    def help_save_game_options(self):
        print('\n'.join(['save_game_options [file_name]', 'Saves the game options used to a json file']))

    def help_cower(self):
        print('\n'.join(['cower', 'Cower to regain 3 health points']))

    def help_next_turn(self):
        print('\n'.join(['next_turn', 'Starts the a turn in the game.',
                         'You will be asked for the door you want to enter on the new tile then,',
                         'You will be asked the door you want to exit on the current tile.',
                         'You then move to that tile and a dev card is draw and the action is played out',
                         'If you happen to die from zombies the game will end.']))

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def help_game_info(self):
        print('\n'.join(['game_info', 'Shows current game information in format below',
                         'Current Tile: [Tile Name]',
                         'Player Health: [Health]',
                         'Player Attack: [Attack Score]',
                         'Player Items: [Items]',
                         'Player Position X: [X Cord], Y: [Y Cord]',
                         ]))
