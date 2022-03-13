from cards.abstract_time_behaviour import AbstractTimeBehaviour


class NeutralTimeBehaviour(AbstractTimeBehaviour):

    def __init__(self, message: str):
        super().__init__(message)

    def action(self):
        return self.message
