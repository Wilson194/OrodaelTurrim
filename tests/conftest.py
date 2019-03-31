from typing import List

import pytest
from antlr4 import InputStream

from ExpertSystem.Business.Parser.KnowledgeBase.RulesLexer import RulesLexer, CommonTokenStream, ParseTreeWalker
from ExpertSystem.Business.Parser.KnowledgeBase.RulesListenerImplementation import RulesListenerImplementation
from ExpertSystem.Business.Parser.KnowledgeBase.RulesParser import RulesParser
from OrodaelTurrim.Business.GameMap import GameMap
from OrodaelTurrim.Structure.Enums import TerrainType
from OrodaelTurrim.Structure.Position import Position


@pytest.fixture
def game_map() -> GameMap:
    tiles = [
        [TerrainType.RIVER, TerrainType.FIELD, TerrainType.FIELD, TerrainType.FOREST, TerrainType.VILLAGE],
        [TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.MOUNTAIN],
        [TerrainType.FOREST, TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.FIELD, TerrainType.RIVER],
        [TerrainType.VILLAGE, TerrainType.MOUNTAIN, TerrainType.HILL, TerrainType.HILL, TerrainType.HILL],
        [TerrainType.RIVER, TerrainType.FIELD, TerrainType.FOREST, TerrainType.FIELD, TerrainType.FOREST],
    ]

    return GameMap(5, 5, tiles)


@pytest.fixture
def utils():
    return Utils()


class Utils:
    def compare_position_list(self, list1: List[Position], list2: List[Position]) -> bool:
        list1 = [x.offset for x in list1]
        list2 = [x.offset for x in list2]
        list1.sort()
        list2.sort()

        return len(set(list1) - set(list2)) == 0 and len(set(list2) - set(list1)) == 0


    def parse_antlr_grammar(self, rule: str):
        input_file = InputStream(rule)

        lexer = RulesLexer(input_file)
        stream = CommonTokenStream(lexer)
        parser = RulesParser(stream)
        tree = parser.rules_set()

        rules_listener = RulesListenerImplementation()
        walker = ParseTreeWalker()
        walker.walk(rules_listener, tree)

        return rules_listener.rules
