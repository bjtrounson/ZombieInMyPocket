import argparse


class Parser:
    args = str

    def __init__(self):
        parser = argparse.ArgumentParser(description='Zombie In My Pocket Game, in Python.')
        parser.add_argument("-hp", "--health", type=int, help="Change starting player health", default=6)
        parser.add_argument("-dmg", "--damage", type=int, help="Change starting player attack damage", default=1)
        self.args = parser.parse_args()
        if self.args.health < 1 or self.args.damage < 1:
            raise ValueError('Player stats cannot be less than 1')