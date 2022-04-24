import dataclasses
import json
import os

from game_options import GameOptions
from pickle_manager.pickle_manager import NoFileNameError


class FileManager:
    def __init__(self, cwd: str):
        self._current_dir = cwd

    def serialize_game_options_to_json(self, file_name: str, game_options: GameOptions) -> None:
        try:
            if file_name != '':
                with open(os.path.join(self._current_dir, f'{file_name}.json'), 'w') as f:
                    json.dump(dataclasses.asdict(game_options), f)
            else:
                raise NoFileNameError
        except NoFileNameError:
            print("You need a file name!! 'save_game [file_name] Try Again'")
        except IOError as e:
            print(f"I/O error({e.errno}): {e.strerror}")
        except Exception as e:
            print(f"Unexpected error writing save file {file_name}", repr(e))

    def deserialize_json_to_game_options(self, file_name: str) -> GameOptions:
        try:
            if file_name != '':
                with open(os.path.join(self._current_dir, f'{file_name}.json'), 'r') as f:
                    options_json = json.loads(f.read())
                    game_options = GameOptions(**options_json)
                return game_options
            else:
                raise NoFileNameError
        except NoFileNameError:
            print("You need a file name!! 'load_game [file_name] Try Again")
        except FileNotFoundError as e:
            print(f"File not found '{file_name}'", repr(e))
        except Exception as e:
            print(f"Unexpected error opening file {file_name}", repr(e))

    def extract_intro_text(self) -> str:
        try:
            with open(os.path.join(self._current_dir, f'intro_text.txt'), 'r') as f:
                intro_text = f.read()
            if isinstance(intro_text, str):
                return intro_text
            else:
                raise ValueError
        except ValueError as e:
            print(f"File did not contain a string", repr(e))
        except FileNotFoundError as e:
            print(f"File not found 'intro_text'", repr(e))
        except Exception as e:
            print(f"Unexpected error opening file intro_text", repr(e))
