from typing import List

from User import ActionBase
from ExpertSystem.Business.UserFramework import IInterference
from OrodaelTurrim.structure.ExpertSystem import Knowledge
from ExpertSystem.Structure.RuleBase import Rule


class Interference(IInterference):
    def interfere(self, knowledge_base: List[Knowledge], rules: List[Rule], action_base: ActionBase):
        print('User inference running')
        print(rules)
