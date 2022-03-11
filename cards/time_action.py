from abstract_time_behaviour import AbstractTimeBehaviour


class TimeAction:
    time: int
    time_behaviour: AbstractTimeBehaviour

    def __init__(self, time: int, time_behaviour: AbstractTimeBehaviour):
        self.time = time
        self.time_behaviour = time_behaviour