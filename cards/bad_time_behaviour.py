from abstract_time_behaviour import AbstractTimeBehaviour


class BadTimeBehaviour(AbstractTimeBehaviour):
    zombies_count: int

    def __init__(self, zombie_count: int):
        self.zombies_count = zombie_count

    def action(self):
        return self.zombies_count
