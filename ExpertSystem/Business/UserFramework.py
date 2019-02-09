from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

from ExpertSystem.Structure.RuleBase import Rule

if TYPE_CHECKING:
    from User.ActionBase import ActionBase
    from OrodaelTurrim.structure.ExpertSystem import Knowledge
    from ExpertSystem.Business.Proxy import ActionProxy, DataProxy


class IKnowledgeBase(ABC):
    def __init__(self, proxy: "DataProxy"):
        self.knowledge_base = []
        self.proxy = proxy

    @abstractmethod
    def create_knowledge_base(self):
        pass


class IInterference(ABC):
    @abstractmethod
    def interfere(self, knowledge_base: List["Knowledge"], rules: List[Rule], action_base: "ActionBase"):
        pass


class IActionBase(ABC):
    def __init__(self, proxy: "ActionProxy"):
        self.proxy = proxy
