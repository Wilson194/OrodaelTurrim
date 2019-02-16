from abc import ABC, abstractmethod
from datetime import datetime

from OrodaelTurrim.business.GameEngine import GameEngine


class GameAction(ABC):
    def __init__(self, game_engine: GameEngine):
        self._game_engine = game_engine
        self.__time_stamp = datetime.timestamp()


    @abstractmethod
    def execute(self):
        pass


    @abstractmethod
    def undo(self):
        pass


    @abstractmethod
    def __str__(self):
        pass
