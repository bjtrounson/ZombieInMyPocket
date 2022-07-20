import doctest

from tests.card_tests.card_tests import CardTestCases
from tests.game_tests.game_tests import GameTestCases
from tests.item_tests.item_tests import ItemTestCases
from tests.pickle_manager_tests.pickle_manager_tests import PickleManagerTestCases
from tests.tile_tests.tile_tests import TileTestCases
from tests.level_tests.level_tests import LevelTestCases
from tests.command_tests import CommandsTestCases

if __name__ == '__main__':
    CardTestCases()
    ItemTestCases()
    TileTestCases()
    LevelTestCases()
    GameTestCases()
    PickleManagerTestCases()
    CommandsTestCases()
    doctest.testmod()
