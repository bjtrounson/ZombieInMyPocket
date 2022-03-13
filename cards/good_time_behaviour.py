from cards.abstract_time_behaviour import AbstractTimeBehaviour


class GoodTimeBehaviour(AbstractTimeBehaviour):
    health: int

    def __init__(self, message: str, health: int):
        super().__init__(message)
        self.health = health

    def action(self):
        return self.health