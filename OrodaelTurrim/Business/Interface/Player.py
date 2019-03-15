from abc import ABC, abstractmethod
from random import Random
from typing import List, TYPE_CHECKING

from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy
from OrodaelTurrim.Structure.Enums import GameRole
if TYPE_CHECKING:
    from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation


class IPlayer(ABC):
    """
    Provides methods for accessing and/or notifying players
    """


    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy, game_control_proxy: GameControlProxy):
        self.map_proxy = map_proxy
        self.game_object_proxy = game_object_proxy
        self.game_control_proxy = game_control_proxy


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


    def __eq__(self, other: "IPlayer"):
        return self.name == other.name and self.role == other.role


    def __hash__(self):
        return hash((self.name, self.role))


class IAttacker(IPlayer, ABC):
    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy, game_control_proxy: GameControlProxy):
        super().__init__(map_proxy, game_object_proxy, game_control_proxy)

        self.spawn_random = Random()  # TODO: Add global seed


    @property
    def role(self) -> GameRole:
        return GameRole.ATTACKER


    @property
    @abstractmethod
    def spawn_information_list(self) -> List[List["SpawnInformation"]]:
        """
        Return list of of spawn information for next 3 rounds
        0 first round
            0 unit 1
            1 Unit 2
            ...
        1 second round
            0 unit 1
            1 Unit 2
            ...
        2 third round
            0 unit 1
            1 Unit 2
            ...
        """
        pass
