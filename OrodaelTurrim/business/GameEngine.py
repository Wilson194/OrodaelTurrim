from typing import List, Dict

from antlr4 import *

from OrodaelTurrim.business.Interface.Player import IPlayer
from OrodaelTurrim.structure.Exceptions import IllegalActionException
from OrodaelTurrim.structure.Map import VisibilityMap
from OrodaelTurrim.structure.Resources import PlayerResources
from User.ActionBase import ActionBase
from User.Interference import Interference
from User.KnowledgeBase import KnowledgeBase
from OrodaelTurrim import USER_ROOT
from OrodaelTurrim.business.GameMap import GameMap
from ExpertSystem.Business.Parser.KnowledgeBase.RulesLexer import RulesLexer
from ExpertSystem.Business.Parser.KnowledgeBase.RulesListener import RulesListener
from ExpertSystem.Business.Parser.KnowledgeBase.RulesParser import RulesParser
from OrodaelTurrim.structure.Enums import AttributeType, GameObjectType, TerrainType
from OrodaelTurrim.structure.GameObjects.GameObject import GameObject, SpawnInformation
from ExpertSystem.Structure.RuleBase import Rule
from OrodaelTurrim.structure.Position import Position
from OrodaelTurrim.structure.TypeStrucutre import TwoWayDict


class GameEngine:
    def __init__(self, turns, game_map: GameMap):
        self.__remaining_turns = turns
        self.__game_map = game_map
        self.__players = []
        self.__player_resources = {}
        self.__player_units = {}
        self.__defender_bases = {}  # type: Dict[IPlayer, GameObject]
        self.__game_object_hit_points = {}
        self.__game_object_effects = {}
        self.__game_object_positions = TwoWayDict()  # type: Dict[Position,GameObject]

        self.__visibility_map = VisibilityMap()

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


    def get_object_visible_tiles(self, game_object: GameObject):
        return self.game_map.get_visible_tiles(self.__game_object_positions[game_object],
                                               int(game_object.get_attribute(AttributeType.SIGH)))


    def get_tiles_in_range(self, game_object: GameObject):
        return self.game_map.get_visible_tiles(self.__game_object_positions[game_object],
                                               int(game_object.get_attribute(AttributeType.RANGE)))


    def get_type(self, position: Position) -> GameObjectType:
        if position not in self.__game_object_positions:
            return GameObjectType.NONE
        return self.__game_object_positions[position].object_type


    def get_current_hit_points(self, position: Position) -> float:
        if position not in self.__game_object_positions:
            return 0.0
        return self.__game_object_positions[position].current_hit_points


    def get_attribute(self, position: Position, attribute_type: AttributeType) -> float:
        if position not in self.__game_object_positions:
            return 0.0
        return self.__game_object_positions[position].get_attribute(attribute_type)


    def get_attack_effect(self, position):
        if position not in self.__game_object_positions:
            return []
        return self.__game_object_positions[position].attack_effects


    def get_resistances(self, position):
        if position not in self.__game_object_positions:
            return []
        return self.__game_object_positions[position]


    def register_player(self, player: IPlayer, resources: PlayerResources, unit_spawn_info: List[SpawnInformation]):
        self.__players.append(player)
        self.__player_resources[player] = resources
        self.__player_units[player] = []

        self.__visibility_map.register_player(player)


    def register_game_object(self, game_object: GameObject):
        owner = game_object.owner
        if game_object.object_type == GameObjectType.BASE:
            if owner in self.__defender_bases:
                raise IllegalActionException('Players are not allowed to spawn multiple bases!')
            else:
                self.__defender_bases[owner] = game_object

        self.__player_units[owner].append(game_object)
        self.__game_object_positions[game_object.position] = game_object


    def compute_attribute(self, game_object: GameObject, attribute_type: AttributeType, original_value: float) -> float:
        affected = self.__game_map[game_object.position].affect_attribute(attribute_type, original_value)

        for effect in game_object.active_effects:
            affected = effect.affect_attribute(attribute_type, affected)

        return affected


    def get_visible_enemies(self, position: Position) -> Dict[Position, int]:
        if position not in self.__game_object_positions:
            return dict()

        return self.__game_object_positions[position].visible_enemies


    @property
    def map_height(self) -> int:
        return self.__game_map.size[1]


    @property
    def map_width(self) -> int:
        return self.__game_map.size[0]


    def get_terrain_type(self, position: Position) -> TerrainType:
        return self.__game_map[position].terrain_type


    def is_position_on_map(self, position: Position) -> bool:
        return self.__game_map.position_on_map(position)


    def is_position_occupied(self, position: Position) -> bool:
        return position in self.__game_object_positions


    @property
    def bases_positions(self):
        """
        Test documentation
        :return:
        """
        return [x.position for x in self.__defender_bases.values()]


    def get_visible_tiles(self, position: Position, sight: int) -> List[Position]:
        return self.__game_map.get_visible_tiles(position, sight)


    def get_accessible_tiles(self, position: Position, actions: int) -> Dict[Position, int]:
        return self.__game_map.get_accessible_tiles(position, actions)


    def create_move_action(self, game_object: GameObject, position: Position):
        if game_object and position:
            pass


    def create_attack_action(self, game_object: GameObject, position: Position):
        pass


    def damage(self, game_object: GameObject, damage: float):
        game_object.take_damage(damage)


    def heal(self, game_object: GameObject, amount: float):
        game_object.receive_healing(amount)


    def move(self, game_object: GameObject, to: Position):
        position_from = game_object.position

        self.__game_object_positions.__delitem__(position_from)
        self.__game_object_positions[to] = game_object

        game_object.position = to
