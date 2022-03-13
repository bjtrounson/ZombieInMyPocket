from cards.time_action import TimeAction


class Card:
    time_actions: list[TimeAction]

    def __init__(self, time_actions: list[TimeAction]):
        if len(time_actions) < 4:
            self.time_actions = time_actions
        else:
            raise Exception("Cannot add more than 3 time actions to the list")

    def get_time_action(self, time: int):
        for action in self.time_actions:
            if action.time == time:
                return action
