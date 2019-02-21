from abc import ABC, abstractmethod
from datetime import datetime

from OrodaelTurrim.Business.GameEngine import GameEngine


class GameAction(ABC):
    TIME_STAMP_FORMAT = '%M:%h:%s'


    def __init__(self, game_engine: GameEngine):
        self._game_engine = game_engine
        self.__time_stamp = datetime.now()


    @abstractmethod
    def execute(self) -> None:
        pass


    @abstractmethod
    def undo(self) -> None:
        pass


    @property
    @abstractmethod
    def text(self) -> str:
        pass


    def __str__(self):
        return '{} : {}'.format(self.__time_stamp.strftime(self.TIME_STAMP_FORMAT), self.text)
