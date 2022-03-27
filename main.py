import cmd
from pprint import pprint
from cards.card_manager import CardManager
from game import Game
from level.level import Level
from parser import Parser
from player import Player

class Main(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.aliases = {'quit': self.quit,
                        'help': self.do_help,
                        'rename': self.rename,
                        'stats': self.stats,
                        'phealth': self.phealth,
                        'pattack': self.pattack}
        parser = Parser()

        self.player = Player(parser.args.health, parser.args.damage, [], 0, 0)
        level = Level([], self.player)

        self.card_manager = CardManager()
        self.card_manager.add_all_cards()

        game = Game(9, level, self.card_manager.get_deck())

        print(self.player.get_attack_score())
        print(self.player.get_health())
        print(self.card_manager.get_deck())
        pprint(vars(self.card_manager.get_deck()[0]))

    def do_help(self, args):
        '''Show commands.'''
        if args in self.aliases:
            args = self.aliases[args].__name__[3:]
            cmd.Cmd.do_help(self, args)
        else:
            print ("Documented commands (type help <topic>):\n========================================")
            for key in self.aliases.keys():
                print(key)
            print("========================================")

    def quit(self, args):
        '''Exit the program.'''
        return True

    def phealth(self, args):
        '''Show player health'''
        print("Health: {}".format(self.player.get_health()))

    def pattack(self, args):
        '''Show player attack damage'''
        print("Attack: {}".format(self.player.get_attack_score()))

    def stats(self, args):
        '''Show player stats'''
        print("Health: {}\nAttack: {}".format(self.player.get_health(), self.player.get_attack_score()))

    def rename(self, args):
        '''Rebind commands'''
        if len(args.split()) > 0:
            cmd = args.split()[0]
        else: cmd = input("Command to rename: ")

        #if "do_{}".format(cmd) in dir(Main):
        if cmd in self.aliases:
            global new_cmd
            if len(args.split()) > 1:
                new_cmd = args.split()[1]
            else: new_cmd = input("New command name: ")
            if new_cmd.isspace():
                raise TypeError("Blank response")
            self.aliases[new_cmd] = self.aliases[cmd]
            del self.aliases[cmd]
            # self.cmd.__name__ = "do_{}".format(new_cmd)
            print("Successfully changed {} to {}".format(cmd, new_cmd))
        else: print("--- Unknown command: {}".format(cmd))


    def default(self, line):
        cmd, args, line = self.parseline(line)
        if cmd in self.aliases:
            return self.aliases[cmd](args)
        else:
            print("--- Unknown command: {}".format(line))

if __name__ == '__main__':
    Main.prompt = 'ZombieInMyPocket$ '
    Main().cmdloop()