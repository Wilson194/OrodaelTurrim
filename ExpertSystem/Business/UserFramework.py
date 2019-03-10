from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING, Any, Set, Union

from ExpertSystem.Structure.RuleBase import Rule, Expression
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


    def __getitem__(self, item: Union[str, Expression]) -> None:
        if type(item) is str:
            getattr(self, item)()
        elif isinstance(item, Expression):
            getattr(self, item.name)(*item.args)


    def __contains__(self, item: Union[str, Expression]) -> bool:
        if type(item) is str:
            if callable(getattr(self, item, None)):
                return True
        elif isinstance(item, Expression):
            if callable(getattr(self, item.name, None)):
                return True

        raise ValueError('Test only with string or Expression')
