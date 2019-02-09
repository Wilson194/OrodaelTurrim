# Generated from Rules.g4 by ANTLR 4.7.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\25")
        buf.write("l\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\3\2\7\2\32\n\2")
        buf.write("\f\2\16\2\35\13\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\4")
        buf.write("\3\4\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\6\5\6\61\n\6\3\6\3")
        buf.write("\6\3\6\3\6\3\6\3\6\7\69\n\6\f\6\16\6<\13\6\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7K\n\7\3\b")
        buf.write("\3\b\3\b\3\b\5\bQ\n\b\3\t\3\t\3\n\3\n\3\13\3\13\3\13\3")
        buf.write("\13\3\13\3\13\5\13]\n\13\3\13\3\13\3\13\7\13b\n\13\f\13")
        buf.write("\16\13e\13\13\3\f\3\f\3\f\5\fj\n\f\3\f\2\4\n\24\r\2\4")
        buf.write("\6\b\n\f\16\20\22\24\26\2\5\3\2\7\b\3\2\21\22\3\2\t\16")
        buf.write("\2l\2\33\3\2\2\2\4 \3\2\2\2\6&\3\2\2\2\b(\3\2\2\2\n\60")
        buf.write("\3\2\2\2\fJ\3\2\2\2\16P\3\2\2\2\20R\3\2\2\2\22T\3\2\2")
        buf.write("\2\24\\\3\2\2\2\26i\3\2\2\2\30\32\5\4\3\2\31\30\3\2\2")
        buf.write("\2\32\35\3\2\2\2\33\31\3\2\2\2\33\34\3\2\2\2\34\36\3\2")
        buf.write("\2\2\35\33\3\2\2\2\36\37\7\2\2\3\37\3\3\2\2\2 !\7\3\2")
        buf.write("\2!\"\5\6\4\2\"#\7\4\2\2#$\5\b\5\2$%\7\23\2\2%\5\3\2\2")
        buf.write("\2&\'\5\n\6\2\'\7\3\2\2\2()\5\24\13\2)\t\3\2\2\2*+\b\6")
        buf.write("\1\2+\61\5\f\7\2,-\7\17\2\2-.\5\n\6\2./\7\20\2\2/\61\3")
        buf.write("\2\2\2\60*\3\2\2\2\60,\3\2\2\2\61:\3\2\2\2\62\63\f\6\2")
        buf.write("\2\63\64\7\5\2\2\649\5\n\6\7\65\66\f\5\2\2\66\67\7\6\2")
        buf.write("\2\679\5\n\6\68\62\3\2\2\28\65\3\2\2\29<\3\2\2\2:8\3\2")
        buf.write("\2\2:;\3\2\2\2;\13\3\2\2\2<:\3\2\2\2=>\7\22\2\2>K\5\16")
        buf.write("\b\2?@\7\22\2\2@A\5\16\b\2AB\5\22\n\2BC\7\21\2\2CK\3\2")
        buf.write("\2\2DK\7\22\2\2EF\7\22\2\2FG\5\22\n\2GH\7\21\2\2HK\3\2")
        buf.write("\2\2IK\t\2\2\2J=\3\2\2\2J?\3\2\2\2JD\3\2\2\2JE\3\2\2\2")
        buf.write("JI\3\2\2\2K\r\3\2\2\2LM\5\20\t\2MN\5\16\b\2NQ\3\2\2\2")
        buf.write("OQ\5\20\t\2PL\3\2\2\2PO\3\2\2\2Q\17\3\2\2\2RS\t\3\2\2")
        buf.write("S\21\3\2\2\2TU\t\4\2\2U\23\3\2\2\2VW\b\13\1\2WX\7\17\2")
        buf.write("\2XY\5\24\13\2YZ\7\20\2\2Z]\3\2\2\2[]\5\26\f\2\\V\3\2")
        buf.write("\2\2\\[\3\2\2\2]c\3\2\2\2^_\f\5\2\2_`\7\5\2\2`b\5\24\13")
        buf.write("\6a^\3\2\2\2be\3\2\2\2ca\3\2\2\2cd\3\2\2\2d\25\3\2\2\2")
        buf.write("ec\3\2\2\2fj\7\22\2\2gh\7\22\2\2hj\5\16\b\2if\3\2\2\2")
        buf.write("ig\3\2\2\2j\27\3\2\2\2\13\33\608:JP\\ci")
        return buf.getvalue()


class RulesParser(Parser):
    grammarFileName = "Rules.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "'IF'", "'THEN'", "'AND'", "'OR'", "'TRUE'",
                    "'FALSE'", "'>'", "'>='", "'<'", "'<='", "'=='", "'!='",
                    "'('", "')'", "<INVALID>", "<INVALID>", "';'"]

    symbolicNames = ["<INVALID>", "IF", "THEN", "AND", "OR", "TRUE", "FALSE",
                     "GT", "GE", "LT", "LE", "EQ", "NE", "LPAREN", "RPAREN",
                     "DECIMAL", "IDENTIFIER", "SEMI", "COMMENT", "WS"]

    RULE_rules_set = 0
    RULE_single_rule = 1
    RULE_condition = 2
    RULE_conclusion = 3
    RULE_left_logical_expr = 4
    RULE_function_expr = 5
    RULE_args = 6
    RULE_arg = 7
    RULE_comp_operator = 8
    RULE_right_logical_expr = 9
    RULE_r_function_expr = 10

    ruleNames = ["rules_set", "single_rule", "condition", "conclusion",
                 "left_logical_expr", "function_expr", "args", "arg",
                 "comp_operator", "right_logical_expr", "r_function_expr"]

    EOF = Token.EOF
    IF = 1
    THEN = 2
    AND = 3
    OR = 4
    TRUE = 5
    FALSE = 6
    GT = 7
    GE = 8
    LT = 9
    LE = 10
    EQ = 11
    NE = 12
    LPAREN = 13
    RPAREN = 14
    DECIMAL = 15
    IDENTIFIER = 16
    SEMI = 17
    COMMENT = 18
    WS = 19

    def __init__(self, input: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None

    class Rules_setContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(RulesParser.EOF, 0)

        def single_rule(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RulesParser.Single_ruleContext)
            else:
                return self.getTypedRuleContext(RulesParser.Single_ruleContext, i)

        def getRuleIndex(self):
            return RulesParser.RULE_rules_set

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterRules_set"):
                listener.enterRules_set(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitRules_set"):
                listener.exitRules_set(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRules_set"):
                return visitor.visitRules_set(self)
            else:
                return visitor.visitChildren(self)

    def rules_set(self):

        localctx = RulesParser.Rules_setContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_rules_set)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 25
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == RulesParser.IF:
                self.state = 22
                self.single_rule()
                self.state = 27
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 28
            self.match(RulesParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Single_ruleContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(RulesParser.IF, 0)

        def condition(self):
            return self.getTypedRuleContext(RulesParser.ConditionContext, 0)

        def THEN(self):
            return self.getToken(RulesParser.THEN, 0)

        def conclusion(self):
            return self.getTypedRuleContext(RulesParser.ConclusionContext, 0)

        def SEMI(self):
            return self.getToken(RulesParser.SEMI, 0)

        def getRuleIndex(self):
            return RulesParser.RULE_single_rule

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterSingle_rule"):
                listener.enterSingle_rule(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitSingle_rule"):
                listener.exitSingle_rule(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitSingle_rule"):
                return visitor.visitSingle_rule(self)
            else:
                return visitor.visitChildren(self)

    def single_rule(self):

        localctx = RulesParser.Single_ruleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_single_rule)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.match(RulesParser.IF)
            self.state = 31
            self.condition()
            self.state = 32
            self.match(RulesParser.THEN)
            self.state = 33
            self.conclusion()
            self.state = 34
            self.match(RulesParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ConditionContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def left_logical_expr(self):
            return self.getTypedRuleContext(RulesParser.Left_logical_exprContext, 0)

        def getRuleIndex(self):
            return RulesParser.RULE_condition

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterCondition"):
                listener.enterCondition(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitCondition"):
                listener.exitCondition(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitCondition"):
                return visitor.visitCondition(self)
            else:
                return visitor.visitChildren(self)

    def condition(self):

        localctx = RulesParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.left_logical_expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ConclusionContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def right_logical_expr(self):
            return self.getTypedRuleContext(RulesParser.Right_logical_exprContext, 0)

        def getRuleIndex(self):
            return RulesParser.RULE_conclusion

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterConclusion"):
                listener.enterConclusion(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitConclusion"):
                listener.exitConclusion(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitConclusion"):
                return visitor.visitConclusion(self)
            else:
                return visitor.visitChildren(self)

    def conclusion(self):

        localctx = RulesParser.ConclusionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_conclusion)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self.right_logical_expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Left_logical_exprContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def getRuleIndex(self):
            return RulesParser.RULE_left_logical_expr

        def copyFrom(self, ctx: ParserRuleContext):
            super().copyFrom(ctx)

    class ComparisonExpressionContext(Left_logical_exprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a RulesParser.Left_logical_exprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def function_expr(self):
            return self.getTypedRuleContext(RulesParser.Function_exprContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterComparisonExpression"):
                listener.enterComparisonExpression(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitComparisonExpression"):
                listener.exitComparisonExpression(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitComparisonExpression"):
                return visitor.visitComparisonExpression(self)
            else:
                return visitor.visitChildren(self)

    class LogicalExpressionInParenContext(Left_logical_exprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a RulesParser.Left_logical_exprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(RulesParser.LPAREN, 0)

        def left_logical_expr(self):
            return self.getTypedRuleContext(RulesParser.Left_logical_exprContext, 0)

        def RPAREN(self):
            return self.getToken(RulesParser.RPAREN, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterLogicalExpressionInParen"):
                listener.enterLogicalExpressionInParen(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitLogicalExpressionInParen"):
                listener.exitLogicalExpressionInParen(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLogicalExpressionInParen"):
                return visitor.visitLogicalExpressionInParen(self)
            else:
                return visitor.visitChildren(self)

    class LogicalExpressionAndContext(Left_logical_exprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a RulesParser.Left_logical_exprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def left_logical_expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RulesParser.Left_logical_exprContext)
            else:
                return self.getTypedRuleContext(RulesParser.Left_logical_exprContext, i)

        def AND(self):
            return self.getToken(RulesParser.AND, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterLogicalExpressionAnd"):
                listener.enterLogicalExpressionAnd(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitLogicalExpressionAnd"):
                listener.exitLogicalExpressionAnd(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLogicalExpressionAnd"):
                return visitor.visitLogicalExpressionAnd(self)
            else:
                return visitor.visitChildren(self)

    class LogicalExpressionOrContext(Left_logical_exprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a RulesParser.Left_logical_exprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def left_logical_expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RulesParser.Left_logical_exprContext)
            else:
                return self.getTypedRuleContext(RulesParser.Left_logical_exprContext, i)

        def OR(self):
            return self.getToken(RulesParser.OR, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterLogicalExpressionOr"):
                listener.enterLogicalExpressionOr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitLogicalExpressionOr"):
                listener.exitLogicalExpressionOr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLogicalExpressionOr"):
                return visitor.visitLogicalExpressionOr(self)
            else:
                return visitor.visitChildren(self)

    def left_logical_expr(self, _p: int = 0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = RulesParser.Left_logical_exprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_left_logical_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [RulesParser.TRUE, RulesParser.FALSE, RulesParser.IDENTIFIER]:
                localctx = RulesParser.ComparisonExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 41
                self.function_expr()
                pass
            elif token in [RulesParser.LPAREN]:
                localctx = RulesParser.LogicalExpressionInParenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 42
                self.match(RulesParser.LPAREN)
                self.state = 43
                self.left_logical_expr(0)
                self.state = 44
                self.match(RulesParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 56
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 3, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 54
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 2, self._ctx)
                    if la_ == 1:
                        localctx = RulesParser.LogicalExpressionAndContext(self,
                                                                           RulesParser.Left_logical_exprContext(self,
                                                                                                                _parentctx,
                                                                                                                _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_left_logical_expr)
                        self.state = 48
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 49
                        self.match(RulesParser.AND)
                        self.state = 50
                        self.left_logical_expr(5)
                        pass

                    elif la_ == 2:
                        localctx = RulesParser.LogicalExpressionOrContext(self,
                                                                          RulesParser.Left_logical_exprContext(self,
                                                                                                               _parentctx,
                                                                                                               _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_left_logical_expr)
                        self.state = 51
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 52
                        self.match(RulesParser.OR)
                        self.state = 53
                        self.left_logical_expr(4)
                        pass

                self.state = 58
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 3, self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class Function_exprContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(RulesParser.IDENTIFIER, 0)

        def args(self):
            return self.getTypedRuleContext(RulesParser.ArgsContext, 0)

        def comp_operator(self):
            return self.getTypedRuleContext(RulesParser.Comp_operatorContext, 0)

        def DECIMAL(self):
            return self.getToken(RulesParser.DECIMAL, 0)

        def TRUE(self):
            return self.getToken(RulesParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(RulesParser.FALSE, 0)

        def getRuleIndex(self):
            return RulesParser.RULE_function_expr

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterFunction_expr"):
                listener.enterFunction_expr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitFunction_expr"):
                listener.exitFunction_expr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFunction_expr"):
                return visitor.visitFunction_expr(self)
            else:
                return visitor.visitChildren(self)

    def function_expr(self):

        localctx = RulesParser.Function_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_function_expr)
        self._la = 0  # Token type
        try:
            self.state = 72
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 4, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 59
                self.match(RulesParser.IDENTIFIER)
                self.state = 60
                self.args()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 61
                self.match(RulesParser.IDENTIFIER)
                self.state = 62
                self.args()
                self.state = 63
                self.comp_operator()
                self.state = 64
                self.match(RulesParser.DECIMAL)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 66
                self.match(RulesParser.IDENTIFIER)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 67
                self.match(RulesParser.IDENTIFIER)
                self.state = 68
                self.comp_operator()
                self.state = 69
                self.match(RulesParser.DECIMAL)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 71
                _la = self._input.LA(1)
                if not (_la == RulesParser.TRUE or _la == RulesParser.FALSE):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArgsContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arg(self):
            return self.getTypedRuleContext(RulesParser.ArgContext, 0)

        def args(self):
            return self.getTypedRuleContext(RulesParser.ArgsContext, 0)

        def getRuleIndex(self):
            return RulesParser.RULE_args

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterArgs"):
                listener.enterArgs(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitArgs"):
                listener.exitArgs(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitArgs"):
                return visitor.visitArgs(self)
            else:
                return visitor.visitChildren(self)

    def args(self):

        localctx = RulesParser.ArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_args)
        try:
            self.state = 78
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 5, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 74
                self.arg()
                self.state = 75
                self.args()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 77
                self.arg()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArgContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DECIMAL(self):
            return self.getToken(RulesParser.DECIMAL, 0)

        def IDENTIFIER(self):
            return self.getToken(RulesParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return RulesParser.RULE_arg

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterArg"):
                listener.enterArg(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitArg"):
                listener.exitArg(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitArg"):
                return visitor.visitArg(self)
            else:
                return visitor.visitChildren(self)

    def arg(self):

        localctx = RulesParser.ArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_arg)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            _la = self._input.LA(1)
            if not (_la == RulesParser.DECIMAL or _la == RulesParser.IDENTIFIER):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Comp_operatorContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GT(self):
            return self.getToken(RulesParser.GT, 0)

        def GE(self):
            return self.getToken(RulesParser.GE, 0)

        def LT(self):
            return self.getToken(RulesParser.LT, 0)

        def LE(self):
            return self.getToken(RulesParser.LE, 0)

        def EQ(self):
            return self.getToken(RulesParser.EQ, 0)

        def NE(self):
            return self.getToken(RulesParser.NE, 0)

        def getRuleIndex(self):
            return RulesParser.RULE_comp_operator

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterComp_operator"):
                listener.enterComp_operator(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitComp_operator"):
                listener.exitComp_operator(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitComp_operator"):
                return visitor.visitComp_operator(self)
            else:
                return visitor.visitChildren(self)

    def comp_operator(self):

        localctx = RulesParser.Comp_operatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_comp_operator)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            _la = self._input.LA(1)
            if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & (
                    (1 << RulesParser.GT) | (1 << RulesParser.GE) | (1 << RulesParser.LT) | (1 << RulesParser.LE) | (
                    1 << RulesParser.EQ) | (1 << RulesParser.NE))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Right_logical_exprContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def getRuleIndex(self):
            return RulesParser.RULE_right_logical_expr

        def copyFrom(self, ctx: ParserRuleContext):
            super().copyFrom(ctx)

    class RLogicalExpressionContext(Right_logical_exprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a RulesParser.Right_logical_exprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def r_function_expr(self):
            return self.getTypedRuleContext(RulesParser.R_function_exprContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterRLogicalExpression"):
                listener.enterRLogicalExpression(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitRLogicalExpression"):
                listener.exitRLogicalExpression(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRLogicalExpression"):
                return visitor.visitRLogicalExpression(self)
            else:
                return visitor.visitChildren(self)

    class RLogicalExpressionAndContext(Right_logical_exprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a RulesParser.Right_logical_exprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def right_logical_expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(RulesParser.Right_logical_exprContext)
            else:
                return self.getTypedRuleContext(RulesParser.Right_logical_exprContext, i)

        def AND(self):
            return self.getToken(RulesParser.AND, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterRLogicalExpressionAnd"):
                listener.enterRLogicalExpressionAnd(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitRLogicalExpressionAnd"):
                listener.exitRLogicalExpressionAnd(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRLogicalExpressionAnd"):
                return visitor.visitRLogicalExpressionAnd(self)
            else:
                return visitor.visitChildren(self)

    class RLogicalExpressionInParenContext(Right_logical_exprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a RulesParser.Right_logical_exprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(RulesParser.LPAREN, 0)

        def right_logical_expr(self):
            return self.getTypedRuleContext(RulesParser.Right_logical_exprContext, 0)

        def RPAREN(self):
            return self.getToken(RulesParser.RPAREN, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterRLogicalExpressionInParen"):
                listener.enterRLogicalExpressionInParen(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitRLogicalExpressionInParen"):
                listener.exitRLogicalExpressionInParen(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRLogicalExpressionInParen"):
                return visitor.visitRLogicalExpressionInParen(self)
            else:
                return visitor.visitChildren(self)

    def right_logical_expr(self, _p: int = 0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = RulesParser.Right_logical_exprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 18
        self.enterRecursionRule(localctx, 18, self.RULE_right_logical_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [RulesParser.LPAREN]:
                localctx = RulesParser.RLogicalExpressionInParenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 85
                self.match(RulesParser.LPAREN)
                self.state = 86
                self.right_logical_expr(0)
                self.state = 87
                self.match(RulesParser.RPAREN)
                pass
            elif token in [RulesParser.IDENTIFIER]:
                localctx = RulesParser.RLogicalExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 89
                self.r_function_expr()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 97
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 7, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = RulesParser.RLogicalExpressionAndContext(self,
                                                                        RulesParser.Right_logical_exprContext(self,
                                                                                                              _parentctx,
                                                                                                              _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_right_logical_expr)
                    self.state = 92
                    if not self.precpred(self._ctx, 3):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                    self.state = 93
                    self.match(RulesParser.AND)
                    self.state = 94
                    self.right_logical_expr(4)
                self.state = 99
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 7, self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class R_function_exprContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(RulesParser.IDENTIFIER, 0)

        def args(self):
            return self.getTypedRuleContext(RulesParser.ArgsContext, 0)

        def getRuleIndex(self):
            return RulesParser.RULE_r_function_expr

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterR_function_expr"):
                listener.enterR_function_expr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitR_function_expr"):
                listener.exitR_function_expr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitR_function_expr"):
                return visitor.visitR_function_expr(self)
            else:
                return visitor.visitChildren(self)

    def r_function_expr(self):

        localctx = RulesParser.R_function_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_r_function_expr)
        try:
            self.state = 103
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 8, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 100
                self.match(RulesParser.IDENTIFIER)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 101
                self.match(RulesParser.IDENTIFIER)
                self.state = 102
                self.args()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    def sempred(self, localctx: RuleContext, ruleIndex: int, predIndex: int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[4] = self.left_logical_expr_sempred
        self._predicates[9] = self.right_logical_expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def left_logical_expr_sempred(self, localctx: Left_logical_exprContext, predIndex: int):
        if predIndex == 0:
            return self.precpred(self._ctx, 4)

        if predIndex == 1:
            return self.precpred(self._ctx, 3)

    def right_logical_expr_sempred(self, localctx: Right_logical_exprContext, predIndex: int):
        if predIndex == 2:
            return self.precpred(self._ctx, 3)
