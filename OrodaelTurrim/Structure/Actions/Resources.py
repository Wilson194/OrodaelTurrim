from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Structure.Actions.Abstract import GameAction


class EarnResourcesAction(GameAction):
    def __init__(self, game_engine: GameEngine, player: IPlayer, amount: int):
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
    def __init__(self, game_engine: GameEngine, player: IPlayer, amount: int):
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
