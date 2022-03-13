from abc import ABC, abstractmethod


class AbstractTimeBehaviour(ABC):
    message: str

    def __init__(self, message: str):
        self.message = message

    @abstractmethod
    def action(self):
        pass