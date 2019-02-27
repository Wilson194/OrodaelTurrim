from abc import ABC, abstractmethod

from OrodaelTurrim.Structure.Enums import GameRole


class IPlayer(ABC):
    """
    Provides methods for accessing and/or notifying players
    """


    @abstractmethod
    def act(self) -> None:
        """
        Resolves a turn of player. This is the player's only opportunity to place units on map
        """
        pass


    @property
    @abstractmethod
    def role(self) -> GameRole:
        """
        Retrieves role of this player
        :return: Role of this player
        """
        pass


    @property
    @abstractmethod
    def name(self) -> str:
        """
        Retrieves name of this player, which should be displayed in UI
        """
        pass


class Player(IPlayer):
    def act(self) -> None:
        pass


    @property
    def role(self) -> GameRole:
        return GameRole.DEFENDER


    @property
    def name(self) -> str:
        return 'Dummy'


class Enemy(IPlayer):
    def act(self) -> None:
        pass


    @property
    def role(self) -> GameRole:
        return GameRole.ATTACKER


    @property
    def name(self) -> str:
        return 'Dummy'
