from abc import ABC, abstractmethod

from OrodaelTurrim.structure.Enums import GameRole


class IPlayer(ABC):
    """
    Provides methods for accessing and/or notifying players
    """

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
