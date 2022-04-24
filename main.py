from commands import Commands

if __name__ == '__main__':
    interpreter = Commands()
    interpreter.prompt = "ZIMP -> "
    interpreter.cmdloop()
