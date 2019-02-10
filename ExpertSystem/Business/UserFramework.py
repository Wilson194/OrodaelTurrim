from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

from ExpertSystem.Structure.RuleBase import Rule

if TYPE_CHECKING:
    from User.ActionBase import ActionBase
    from OrodaelTurrim.structure.ExpertSystem import Fact
    from ExpertSystem.Business.Proxy import ActionProxy, DataProxy


class IKnowledgeBase(ABC):
    def __init__(self, proxy: "DataProxy"):
        self.fact_base = []
        self.proxy = proxy

    @abstractmethod
    def create_knowledge_base(self):
        pass


class IInterference(ABC):
    @abstractmethod
    def interfere(self, fact_base: List["Fact"], rules: List[Rule], action_base: "ActionBase"):
        pass


class IActionBase(ABC):
    def __init__(self, proxy: "ActionProxy"):
        self.proxy = proxy
