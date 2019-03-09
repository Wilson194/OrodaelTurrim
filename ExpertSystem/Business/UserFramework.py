from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING, Any, Set

from ExpertSystem.Structure.RuleBase import Rule
from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy

if TYPE_CHECKING:
    from User.ActionBase import ActionBase


class IKnowledgeBase(ABC):
    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy, player: IPlayer):
        self.fact_base = []
        self.map_proxy = map_proxy
        self.game_object_proxy = game_object_proxy
        self.player = player


    @abstractmethod
    def create_knowledge_base(self):
        pass


class IInterference(ABC):
    @abstractmethod
    def interfere(self, fact_base: Set[Any], rules: List[Rule], action_base: "ActionBase"):
        pass


class IActionBase(ABC):
    def __init__(self, game_control_proxy: GameControlProxy, player: IPlayer):
        self.game_control_proxy = game_control_proxy
        self.player = player
