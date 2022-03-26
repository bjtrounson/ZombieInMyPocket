import os
import pickle

from game import Game


class NoFileNameError(Exception):
    pass


class PickleManager:
    def __init__(self):
        self._current_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def serialize_object_to_file(self, file_name: str, obj: Game) -> None:
        """

        :param file_name: str
        :param obj: Game
        :return: None

        """
        if file_name != '':
            with open(os.path.join(self._current_dir, f'{file_name}.pkl'), 'wb', 0) as f:
                print("Saving this might take a bit...")
                pickle.dump(obj, f)
            print("Saving finished!!")
        else:
            raise NoFileNameError

    def deserialize_file_to_object(self, file_name: str) -> Game:
        if file_name != '':
            with open(os.path.join(self._current_dir, f'{file_name}.pkl'), 'rb') as f:
                game = pickle.load(f)
            return game
        else:
            raise NoFileNameError
