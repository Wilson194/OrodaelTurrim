from typing import List

from antlr4 import *

from User.ActionBase import ActionBase
from User.Interference import Interference
from User.KnowledgeBase import KnowledgeBase
from OrodaelTurrim import USER_ROOT
from OrodaelTurrim.business.GameMap import GameMap
from ExpertSystem.Business.Parser.KnowledgeBase.RulesLexer import RulesLexer
from ExpertSystem.Business.Parser.KnowledgeBase.RulesListener import RulesListener
from ExpertSystem.Business.Parser.KnowledgeBase.RulesParser import RulesParser
from OrodaelTurrim.structure.Enums import AttributeType
from OrodaelTurrim.structure.GameObject import GameObject
from ExpertSystem.Structure.RuleBase import Rule
from OrodaelTurrim.structure.Position import Position
from OrodaelTurrim.structure.TypeStrucutre import TwoWayDict


class GameEngine:
    def __init__(self, turns, game_map: GameMap):
        self.__remaining_turns = turns
        self.__game_map = game_map
        self.__players = []
        self.__player_resources = {}
        self.__player_incomes = {}
        self.__player_units = {}
        self.__defender_bases = {}
        self.__game_object_hit_points = {}
        self.__game_object_effects = {}
        self.__game_object_positions = TwoWayDict()

        self.__interference = Interference()

        # Initialize knowledge base
        from ExpertSystem.Business.Proxy import DataProxy
        data_proxy = DataProxy(self)
        self.__knowledge_base = KnowledgeBase(data_proxy)

        # Initialize action base
        from ExpertSystem.Business.Proxy import ActionProxy
        proxy = ActionProxy(self)
        self.__action_base = ActionBase(proxy)

    def inference_turn(self):
        # Create knowledge base for current turn
        self.__knowledge_base.create_knowledge_base()
        knowledge_base = self.__knowledge_base.knowledge_base

        rules = self.__parse_rules_file()
        # print(rules)

        # Start interference
        self.__interference.interfere(knowledge_base, rules, self.__action_base)

    def __parse_rules_file(self) -> List[Rule]:
        input_file = FileStream(str(USER_ROOT / 'rules'))
        lexer = RulesLexer(input_file)
        stream = CommonTokenStream(lexer)
        parser = RulesParser(stream)
        tree = parser.rules_set()

        rules_listener = RulesListener()
        walker = ParseTreeWalker()
        walker.walk(rules_listener, tree)

        rules = rules_listener.rules

        return rules

    @property
    def game_map(self):
        return self.__game_map

    @game_map.setter
    def game_map(self, value):
        self.__game_map = value

    def get_bases_positions(self) -> List[Position]:
        positions = []

        for base in self.__defender_bases:
            positions.append(self.__game_object_positions[base])

        return positions

    def get_visible_tiles(self, game_object: GameObject):
        return self.game_map.get_visible_tiles(self.__game_object_positions[game_object],
                                               int(game_object.get_attribute(AttributeType.SIGH)))

    def get_tiles_in_range(self, game_object: GameObject):
        return self.game_map.get_visible_tiles(self.__game_object_positions[game_object],
                                               int(game_object.get_attribute(AttributeType.RANGE)))
