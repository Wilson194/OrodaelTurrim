from typing import List

from User import ActionBase
from ZNS.User.UserFramework import IInterference
from ZNS.structure.ExpertSystem import Knowledge
from ZNS.structure.Parser.RuleBase import Rule


class Interference(IInterference):
    def interfere(self, knowledge_base: List[Knowledge], rules: List[Rule], action_base: ActionBase):
        print('User inference running')
        print(rules)
