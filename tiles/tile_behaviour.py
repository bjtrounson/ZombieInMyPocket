from abc import ABC, abstractmethod


class TileBehaviour(ABC):
    
    @abstractmethod
    def action(self):
        pass
