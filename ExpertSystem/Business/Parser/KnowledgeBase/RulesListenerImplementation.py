# Generated from Rules.g4 by ANTLR 4.7.1
from antlr4 import *

from ExpertSystem.Business.Parser.KnowledgeBase.RulesListener import RulesListener
from ExpertSystem.Structure.Enums import LogicalOperator
from ExpertSystem.Structure.RuleBase import Rule, Expression, ExpressionNode

if __name__ is not None and "." in __name__:
    from .RulesParser import RulesParser
else:
    from RulesParser import RulesParser


# This class defines a complete listener for a parse tree produced by RulesParser.
class RulesListenerImplementation(RulesListener):
    def __init__(self):
        super().__init__()
        self.rules = None
        self.rule = None
        self.expression = None
        self.context = None
        self.expression_uncertainty = None


    # Enter a parse tree produced by RulesParser#rules_set.
    def enterRules_set(self, ctx: RulesParser.Rules_setContext):
        self.rules = []


    # Exit a parse tree produced by RulesParser#rules_set.
    def exitRules_set(self, ctx: RulesParser.Rules_setContext):
        pass


    # Enter a parse tree produced by RulesParser#single_rule.
    def enterSingle_rule(self, ctx: RulesParser.Single_ruleContext):
        self.rule = Rule()
        if ctx.WITH() and ctx.DECIMAL() and 'missing' not in ctx.DECIMAL().getText():
            self.rule.uncertainty = float(ctx.DECIMAL().getText())


    # Exit a parse tree produced by RulesParser#single_rule.
    def exitSingle_rule(self, ctx: RulesParser.Single_ruleContext):
        self.rules.append(self.rule)


    # Enter a parse tree produced by RulesParser#condition.
    def enterCondition(self, ctx: RulesParser.ConditionContext):
        self.context = ExpressionNode()
        self.rule.condition = self.context


    # Exit a parse tree produced by RulesParser#condition.
    def exitCondition(self, ctx: RulesParser.ConditionContext):
        pass


    # Enter a parse tree produced by RulesParser#conclusion.
    def enterConclusion(self, ctx: RulesParser.ConclusionContext):
        self.context = ExpressionNode()
        self.rule.conclusion = self.context


    # Exit a parse tree produced by RulesParser#conclusion.
    def exitConclusion(self, ctx: RulesParser.ConclusionContext):
        pass


    # Enter a parse tree produced by RulesParser#ComparisonExpression.
    def enterComparisonExpression(self, ctx: RulesParser.ComparisonExpressionContext):
        self.expression_uncertainty = ctx.DECIMAL()


    # Exit a parse tree produced by RulesParser#ComparisonExpression.
    def exitComparisonExpression(self, ctx: RulesParser.ComparisonExpressionContext):
        self.expression_uncertainty = None


    # Enter a parse tree produced by RulesParser#LogicalExpressionInParen.
    def enterLogicalExpressionInParen(self, ctx: RulesParser.LogicalExpressionInParenContext):
        self.context.parentheses = True


    # Exit a parse tree produced by RulesParser#LogicalExpressionInParen.
    def exitLogicalExpressionInParen(self, ctx: RulesParser.LogicalExpressionInParenContext):
        pass


    # Enter a parse tree produced by RulesParser#LogicalExpressionAnd.
    def enterLogicalExpressionAnd(self, ctx: RulesParser.LogicalExpressionAndContext):
        self.context.value = LogicalOperator.AND
        self.context.left = ExpressionNode()
        self.context.left.parent = self.context
        self.context = self.context.left


    # Exit a parse tree produced by RulesParser#LogicalExpressionAnd.
    def exitLogicalExpressionAnd(self, ctx: RulesParser.LogicalExpressionAndContext):
        if self.context.parent:
            if self.context.parent.right is None:
                self.context.parent.right = ExpressionNode()
                self.context.parent.right.parent = self.context.parent
                self.context = self.context.parent.right
            else:
                self.context = self.context.parent


    # Enter a parse tree produced by RulesParser#LogicalExpressionOr.
    def enterLogicalExpressionOr(self, ctx: RulesParser.LogicalExpressionOrContext):
        self.context.value = LogicalOperator.OR
        self.context.left = ExpressionNode()
        self.context.left.parent = self.context
        self.context = self.context.left


    # Exit a parse tree produced by RulesParser#LogicalExpressionOr.
    def exitLogicalExpressionOr(self, ctx: RulesParser.LogicalExpressionOrContext):
        if self.context.parent:
            if self.context.parent.right is None:
                self.context.parent.right = ExpressionNode()
                self.context.parent.right.parent = self.context.parent
                self.context = self.context.parent.right
            else:
                self.context = self.context.parent


    # Enter a parse tree produced by RulesParser#function_expr.
    def enterFunction_expr(self, ctx: RulesParser.Function_exprContext):
        expression = Expression()
        if self.expression_uncertainty:
            expression.uncertainty = float(self.expression_uncertainty.getText())

        if ctx.IDENTIFIER():
            expression.name = ctx.IDENTIFIER(0).getText()
        else:
            expression.name = 'TRUE' if ctx.TRUE() else 'FALSE'

        if ctx.comp_operator():
            expression.comparator = ctx.comp_operator().getText()

        if ctx.DECIMAL():
            expression.value = ctx.DECIMAL().getText()
        elif len(ctx.IDENTIFIER()) > 1:
            expression.value = ctx.IDENTIFIER(1).getText()

        if ctx.args():
            expression.args = [x.getText() for x in ctx.args().getChildren()]

        self.context.value = expression


    # Exit a parse tree produced by RulesParser#function_expr.
    def exitFunction_expr(self, ctx: RulesParser.Function_exprContext):
        if self.context.parent:
            if self.context.parent.right is None:
                self.context.parent.right = ExpressionNode()
                self.context.parent.right.parent = self.context.parent
                self.context = self.context.parent.right
            else:
                self.context = self.context.parent


    # Enter a parse tree produced by RulesParser#args.
    def enterArgs(self, ctx: RulesParser.ArgsContext):
        pass


    # Exit a parse tree produced by RulesParser#args.
    def exitArgs(self, ctx: RulesParser.ArgsContext):
        pass


    # Enter a parse tree produced by RulesParser#arg.
    def enterArg(self, ctx: RulesParser.ArgContext):
        pass


    # Exit a parse tree produced by RulesParser#arg.
    def exitArg(self, ctx: RulesParser.ArgContext):
        pass


    # Enter a parse tree produced by RulesParser#comp_operator.
    def enterComp_operator(self, ctx: RulesParser.Comp_operatorContext):
        pass


    # Exit a parse tree produced by RulesParser#comp_operator.
    def exitComp_operator(self, ctx: RulesParser.Comp_operatorContext):
        pass


    # Enter a parse tree produced by RulesParser#RLogicalExpression.
    def enterRLogicalExpression(self, ctx: RulesParser.RLogicalExpressionContext):
        pass


    # Exit a parse tree produced by RulesParser#RLogicalExpression.
    def exitRLogicalExpression(self, ctx: RulesParser.RLogicalExpressionContext):
        pass


    # Enter a parse tree produced by RulesParser#RLogicalExpressionAnd.
    def enterRLogicalExpressionAnd(self, ctx: RulesParser.RLogicalExpressionAndContext):
        self.context.value = 'AND'
        self.context.left = ExpressionNode()
        self.context.left.parent = self.context
        self.context = self.context.left


    # Exit a parse tree produced by RulesParser#RLogicalExpressionAnd.
    def exitRLogicalExpressionAnd(self, ctx: RulesParser.RLogicalExpressionAndContext):
        if self.context.parent.parent:
            self.context.parent.parent.right = ExpressionNode()
            self.context.parent.parent.right.parent = self.context.parent.parent
            self.context = self.context.parent.parent.right


    # Enter a parse tree produced by RulesParser#RLogicalExpressionInParen.
    def enterRLogicalExpressionInParen(self, ctx: RulesParser.RLogicalExpressionInParenContext):
        self.context.parentheses = True


    # Exit a parse tree produced by RulesParser#RLogicalExpressionInParen.
    def exitRLogicalExpressionInParen(self, ctx: RulesParser.RLogicalExpressionInParenContext):
        pass


    # Enter a parse tree produced by RulesParser#r_function_expr.
    def enterR_function_expr(self, ctx: RulesParser.R_function_exprContext):
        expression = Expression()

        expression.name = ctx.IDENTIFIER(0).getText()

        if ctx.args():
            expression.args = [x.getText() for x in ctx.args().getChildren()]

        # if ctx.ASSIGN():
        #     expression.comparator = '='
        #
        # if ctx.DECIMAL():
        #     expression.value = ctx.DECIMAL().getText()
        #
        # if ctx.IDENTIFIER(1):
        #     expression.value = ctx.IDENTIFIER(1).getText()

        self.context.value = expression


    # Exit a parse tree produced by RulesParser#r_function_expr.
    def exitR_function_expr(self, ctx: RulesParser.R_function_exprContext):
        if self.context.parent and self.context.parent.right is None:
            self.context.parent.right = ExpressionNode()
            self.context.parent.right.parent = self.context.parent
            self.context = self.context.parent.right
