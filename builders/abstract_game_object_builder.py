from abc import ABC, abstractmethod


class AbstractGameObjectBuilder(ABC):
    @abstractmethod
    def build_game_object(self, object_type):
        pass
