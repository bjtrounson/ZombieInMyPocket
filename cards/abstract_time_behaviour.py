from abc import ABC, abstractmethod


class AbstractTimeBehaviour(ABC):

    @abstractmethod
    def action(self):
        pass