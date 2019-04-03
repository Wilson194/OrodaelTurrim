from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from OrodaelTurrim.Business.GameEngine import GameEngine


class GameAction(ABC):
    """ Core class defining methods for game actions (history marks) """
    TIME_STAMP_FORMAT = '%H:%M:%S'


    def __init__(self, game_engine: "GameEngine"):
        self._game_engine = game_engine
        self.__time_stamp = datetime.now()


    @abstractmethod
    def execute(self) -> None:
        """ Executes given game action """
        pass


    @abstractmethod
    def undo(self) -> None:
        """
        Undoes any effects, which this game action caused effectively returning game to the state
        before this action happened
        """
        pass


    @property
    @abstractmethod
    def text(self) -> str:
        """ Returns text representation of this game action to show, what happened """
        pass


    def __str__(self):
        return '{} : {}'.format(self.__time_stamp.strftime(self.TIME_STAMP_FORMAT), self.text)
