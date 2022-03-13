from cards.abstract_time_behaviour import AbstractTimeBehaviour


class TimeAction:
    time: int
    time_behaviour: AbstractTimeBehaviour

    def __init__(self, time: int, time_behaviour: AbstractTimeBehaviour):
        self.time_behaviour = time_behaviour
        self.time = time

    def __eq__(self, other):
        return self.time == other.time and \
               self.time_behaviour == other.time_behaviour
