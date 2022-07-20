import os

from commands.file_commands import FileCommands
from commands.game_commands import GameCommands
from commands.help_commands import HelpCommands


class Interpreter(HelpCommands, GameCommands, FileCommands):
    def __init__(self):
        super().__init__(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))))

    def preloop(self) -> None:
        intro: str = self._file_manager.extract_intro_text()
        print(intro)
        super(Interpreter, self).preloop()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def do_EOF(self, line):
        """Exit Program"""
        return True
