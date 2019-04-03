from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Structure.Actions.Abstract import GameAction

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from OrodaelTurrim.Business.GameEngine import GameEngine


class EarnResourcesAction(GameAction):
    """ Represents game action of player earning resources """


    def __init__(self, game_engine: "GameEngine", player: IPlayer, amount: int):
        super().__init__(game_engine)
        self.__amount = amount
        self.__player = player


    def execute(self) -> None:
        self._game_engine.earn(self.__player, self.__amount)


    def undo(self) -> None:
        self._game_engine.spend(self.__player, self.__amount)


    @property
    def text(self) -> str:
        return 'Player {} earned {} resources'.format(self.__player.name, self.__amount)


class SpendResourcesAction(GameAction):
    """ Represents game action of player spending resources """


    def __init__(self, game_engine: "GameEngine", player: IPlayer, amount: int):
        super().__init__(game_engine)
        self.__amount = amount
        self.__player = player


    def execute(self) -> None:
        self._game_engine.spend(self.__player, self.__amount)


    def undo(self) -> None:
        self._game_engine.earn(self.__player, self.__amount)


    @property
    def text(self) -> str:
        return 'Player {} spent {} resources'.format(self.__player.name, self.__amount)
