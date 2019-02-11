from typing import List


from User import ActionBase
from ExpertSystem.Business.UserFramework import IInterference
from ExpertSystem.Structure.RuleBase import Rule, Fact


class Interference(IInterference):
    def interfere(self, knowledge_base: List[Fact], rules: List[Rule], action_base: ActionBase):
        print('User inference running')
        print(rules)
