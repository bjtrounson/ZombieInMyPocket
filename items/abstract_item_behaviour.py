from abc import ABC, abstractmethod


class AbstractItemBehaviour(ABC):

    @abstractmethod
    def action(self):
        pass