from typing import List, Set

from ExpertSystem.Business.UserFramework import IKnowledgeBase
from ExpertSystem.Structure.RuleBase import Fact


class KnowledgeBase(IKnowledgeBase):  # TODO: Add description of proxy
    """
    Class for defining known facts based on Proxy information. You can transform here any information from
    proxy to better format of Facts. Important is method `create_knowledge_base()`. Return value of this method
    will be passed to `Interference.interfere`. It is recommended to use Fact class but you can use another type.

    |
    |
    | Class provides attributes:

    - **map_proxy [MapProxy]** -
    - **game_object_proxy [GameObjectProxy]** -
    - **uncertainty_proxy [UncertaintyProxy]** -
    - **player [IPlayer]** - instance of user player for identification in proxy methods

    """


    def create_knowledge_base(self) -> List[Fact]:
        """ Method for create knowledge base """

        facts = []

        if not self.map_proxy.player_have_base(self.player):
            facts.append(Fact('player_dont_have_base'))

        return facts
