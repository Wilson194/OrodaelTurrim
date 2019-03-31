from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker

from ExpertSystem.Business.Parser.KnowledgeBase.ErrorListener import CustomErrorListener
from ExpertSystem.Business.Parser.KnowledgeBase.RulesLexer import RulesLexer
from ExpertSystem.Business.Parser.KnowledgeBase.RulesListenerImplementation import RulesListenerImplementation
from ExpertSystem.Business.Parser.KnowledgeBase.RulesParser import RulesParser
from OrodaelTurrim import USER_ROOT
from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy, GameUncertaintyProxy
from OrodaelTurrim.Structure.Enums import GameRole
from User.ActionBase import ActionBase
from User.Interference import Interference
from User.KnowledgeBase import KnowledgeBase


class Player(IPlayer):
    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy, game_control_proxy: GameControlProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy):
        super().__init__(map_proxy, game_object_proxy, game_control_proxy, game_uncertainty_proxy)

        self.knowledge_base = KnowledgeBase(map_proxy, game_object_proxy, self)
        self.interference = Interference()
        self.action_base = ActionBase(game_control_proxy, self)


    def act(self) -> None:
        knowledge = self.knowledge_base.create_knowledge_base()
        self.interference.interfere(knowledge, self.__parse_rules(), self.action_base)


    @property
    def role(self) -> GameRole:
        return GameRole.DEFENDER


    @property
    def name(self) -> str:
        return 'Student'


    def __parse_rules(self):
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
