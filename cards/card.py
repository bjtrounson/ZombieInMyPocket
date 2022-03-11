from time_action import TimeAction


class Card:
    time_actions: list[TimeAction]

    def __init__(self, time_actions: list[TimeAction]):
        self.time_actions = time_actions
