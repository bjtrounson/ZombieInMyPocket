import argparse
from argparse import ArgumentParser


class Parser:
    args = str
    parser: ArgumentParser

    def __init__(self):
        self.parser = ArgumentParser(description='Zombie In My Pocket Game, in Python.')

    def add_args(self):
        self.parser.add_argument("-hp", "--health", type=int, help="Change starting player health", default=6)
        self.parser.add_argument("-dmg", "--damage", type=int, help="Change starting player attack damage", default=1)
        self.parser.add_argument("-limit", "--item_limit", type=int, help="Change players inventory item limit",
                                 default=2)
        self.parser.add_argument("-start", "--start_time", type=int, help="Change the game start time", default=9)
        self.parser.add_argument("-end", "--end_time", type=int, help="Change the game end time", default=11)
        self.args = self.parser.parse_args()
        if self.args.health < 1 or self.args.damage < 1 or self.args.item_limit < 1 or self.args.start_time < 1 \
                or self.args.end_time < 1:
            raise ValueError('Player stats cannot be less than 1')
