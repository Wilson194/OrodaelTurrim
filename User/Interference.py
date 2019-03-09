from typing import List, Set

from User import ActionBase
from ExpertSystem.Business.UserFramework import IInterference
from ExpertSystem.Structure.RuleBase import Rule, Fact

expressions = {
    'A': True,
    'B': True,
    'C': False,
    'D': True,
}


class Interference(IInterference):
    def interfere(self, knowledge_base: Set[Fact], rules: List[Rule], action_base: ActionBase):
        print('User inference running')

        print(rules[0])
        print(rules[0].condition.left)
        print(type(rules[0].condition.right.right))
        # for rule in rules:
        #     print(self.eval_rule(rule.condition))


    def eval_rule(self, rule):
        if rule.value is None:
            return True

        if rule.value == 'AND':
            return self.eval_rule(rule.left) and self.eval_rule(rule.right)

        if rule.value == 'OR':
            return self.eval_rule(rule.left) or self.eval_rule(rule.right)

        print(type(rule.value))
        print('---->', rule.value)
        return expressions[str(rule.value.name)]
