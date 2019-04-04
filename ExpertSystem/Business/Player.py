import sys

from PyQt5.QtCore import QObject
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker

from ExpertSystem.Business.Parser.KnowledgeBase.ErrorListener import CustomErrorListener
from ExpertSystem.Business.Parser.KnowledgeBase.RulesLexer import RulesLexer
from ExpertSystem.Business.Parser.KnowledgeBase.RulesListenerImplementation import RulesListenerImplementation
from ExpertSystem.Business.Parser.KnowledgeBase.RulesParser import RulesParser
from OrodaelTurrim import USER_ROOT
from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy, GameUncertaintyProxy
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Structure.Enums import GameRole
from User.ActionBase import ActionBase
from User.Interference import Interference
from User.KnowledgeBase import KnowledgeBase


class Player(IPlayer):
    """ Override IPlayer for interference player """


    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy, game_control_proxy: GameControlProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy):
        super().__init__(map_proxy, game_object_proxy, game_control_proxy, game_uncertainty_proxy)

        self.knowledge_base = KnowledgeBase(map_proxy, game_object_proxy, self)
        self.interference = Interference()
        self.action_base = ActionBase(game_control_proxy, self)


    def act(self) -> None:
        """
        Execute on user action round

        * Call create_knowledge_base from user knowledge base
        * Parse rules from rules file
        * Run user interference method with knowledge, parsed rules and action base
        """
        knowledge = self.knowledge_base.create_knowledge_base()
        rules = self.__parse_rules()

        if rules is None:
            sys.stderr.write('Rules file not found! Stopping interference!\n')
            Connector().emit('error_message', 'Interference error', 'Rules file not found! Stopping interference!')
            return
        self.interference.interfere(knowledge, self.__parse_rules(), self.action_base)


    @property
    def role(self) -> GameRole:
        """ Role is defender """
        return GameRole.DEFENDER


    @property
    def name(self) -> str:
        """ Name of the player """
        return 'Student'


    def __parse_rules(self):
        """ Parse rules with antlr4 from rules file """
        if not (USER_ROOT / 'rules').exists():
            return None
        input_file = FileStream(str(USER_ROOT / 'rules'))

        lexer = RulesLexer(input_file)
        stream = CommonTokenStream(lexer)
        parser = RulesParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(CustomErrorListener())
        tree = parser.rules_set()

        rules_listener = RulesListenerImplementation()
        walker = ParseTreeWalker()
        walker.walk(rules_listener, tree)

        rules = rules_listener.rules

        return rules
