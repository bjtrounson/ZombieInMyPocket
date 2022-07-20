from interpreter import Interpreter

if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.prompt = "ZIMP -> "
    interpreter.cmdloop()
