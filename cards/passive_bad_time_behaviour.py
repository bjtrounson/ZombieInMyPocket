from cards.abstract_time_behaviour import AbstractTimeBehaviour


class PassiveBadTimeBehaviour(AbstractTimeBehaviour):
    damage: int

    def __init__(self, damage: int, message: str):
        super().__init__(message)
        self.damage = damage

    def action(self) -> int:
        return self.damage
