from typing import List, Set

from ExpertSystem.Structure.Enums import LogicalOperator
from User import ActionBase
from ExpertSystem.Business.UserFramework import IInterference
from ExpertSystem.Structure.RuleBase import Rule, Fact, ExpressionNode, Expression


class Interference(IInterference):
    def __init__(self):
        self.knowledge_base = None
        self.action_base = None


    def interfere(self, knowledge_base: List[Fact], rules: List[Rule], action_base: ActionBase):
        self.knowledge_base = knowledge_base
        self.action_base = action_base

        for rule in rules:
            condition = self.rule_evaluation(rule.condition)

            if condition and rule.conclusion.value in self.action_base:
                _ = self.action_base[rule.conclusion.value]


    def rule_evaluation(self, root_node: ExpressionNode):
        if root_node.value == LogicalOperator.AND:
            return self.rule_evaluation(root_node.left) and self.rule_evaluation(root_node.right)

        elif root_node.value == LogicalOperator.OR:
            return self.rule_evaluation(root_node.left) or self.rule_evaluation(root_node.right)

        elif isinstance(root_node.value, Expression):
            try:
                return self.knowledge_base[self.knowledge_base.index(root_node.value.name)](*root_node.value.args)
            except ValueError:
                return False

        else:
            return bool(root_node.value)
