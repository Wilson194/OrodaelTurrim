from ExpertSystem.Business.UserFramework import IKnowledgeBase
from typing import List, Any, Set

from ExpertSystem.Structure.RuleBase import Fact


class KnowledgeBase(IKnowledgeBase):
    def create_knowledge_base(self) -> List[Fact]:
        facts = list()

        if not self.map_proxy.player_have_base(self.player):
            facts.append(Fact('player_dont_have_base'))

        return facts
