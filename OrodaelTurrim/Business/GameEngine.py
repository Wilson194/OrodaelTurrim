import copy
from typing import List, Dict, Set

from antlr4 import *

from OrodaelTurrim.Business.Factory import EffectFactory
from OrodaelTurrim.Business.History import GameHistory
from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Structure.Actions.Abstract import GameAction
from OrodaelTurrim.Structure.Actions.Effect import EffectRefreshAction, EffectApplyAction
from OrodaelTurrim.Structure.Exceptions import IllegalActionException
from OrodaelTurrim.Structure.GameObjects.Effect import Effect
from OrodaelTurrim.Structure.Map import VisibilityMap
from OrodaelTurrim.Structure.Resources import PlayerResources
from User.ActionBase import ActionBase
from User.Interference import Interference
from User.KnowledgeBase import KnowledgeBase
from OrodaelTurrim import USER_ROOT
from OrodaelTurrim.Business.GameMap import GameMap
from ExpertSystem.Business.Parser.KnowledgeBase.RulesLexer import RulesLexer
from ExpertSystem.Business.Parser.KnowledgeBase.RulesListener import RulesListener
from ExpertSystem.Business.Parser.KnowledgeBase.RulesParser import RulesParser
from OrodaelTurrim.Structure.Enums import AttributeType, GameObjectType, TerrainType, EffectType, GameRole
from OrodaelTurrim.Structure.GameObjects.GameObject import GameObject, SpawnInformation
from ExpertSystem.Structure.RuleBase import Rule
from OrodaelTurrim.Structure.Position import Position
from OrodaelTurrim.Structure.TypeStrucutre import TwoWayDict


class GameEngine:
    def __init__(self, turns, game_map: GameMap):
        self.__remaining_turns = turns
        self.__game_map = game_map
        self.__players = []
        self.__player_resources = {}
        self.__player_units = {}  # type: Dict[IPlayer, List[GameObject]]
        self.__defender_bases = {}  # type: Dict[IPlayer, GameObject]
        self.__game_object_hit_points = {}
        self.__game_object_effects = {}
        self.__game_object_positions = TwoWayDict()  # type: Dict[Position,GameObject]

        self.__game_history = None  # type: GameHistory

        self.__visibility_map = VisibilityMap()


    def start(self, turn_limit: int) -> None:
        self.__game_history = GameHistory(turn_limit, self.__players)


    def register_player(self, player: IPlayer, resources: PlayerResources,
                        unit_spawn_info: List[SpawnInformation]) -> None:
        self.__players.append(player)
        self.__player_resources[player] = resources
        self.__player_units[player] = []

        self.__visibility_map.register_player(player)

        for spawn_information in unit_spawn_info:
            game_object = GameObject(spawn_information.owner, spawn_information.position, spawn_information.object_type,
                                     self)
            self.register_game_object(game_object)


    def register_game_object(self, game_object: GameObject) -> None:
        owner = game_object.owner
        if game_object.object_type == GameObjectType.BASE:
            if owner in self.__defender_bases:
                raise IllegalActionException('Players are not allowed to spawn multiple bases!')
            else:
                self.__defender_bases[owner] = game_object

        self.__player_units[owner].append(game_object)
        self.__game_object_positions[game_object.position] = game_object

        self.__visibility_map.add_vision(game_object.position, game_object.visible_tiles)

        self.handle_self_vision_gain(game_object, set(), game_object.visible_tiles)
        self.handle_enemy_vision_gain(game_object, game_object.position)


    def delete_game_object(self, game_object: GameObject) -> None:
        self.__player_units[game_object.owner].remove(game_object)
        self.__game_object_positions.pop(game_object.position)

        self.__visibility_map.remove_vision(game_object, game_object.visible_tiles)

        self.handle_self_vision_loss(game_object, game_object.visible_tiles, set())
        self.handle_enemy_vision_loss(game_object, game_object.position)


    def create_unit(self, spawn_information: SpawnInformation) -> GameObject:
        unit = GameObject(spawn_information.owner, copy.deepcopy(spawn_information.position),
                          spawn_information.object_type, self)

        for attack_filter in spawn_information.attack_filters:
            unit.register_attack_filter(attack_filter)

        for move_filter in spawn_information.move_filters:
            unit.register_move_filter(move_filter)

        return unit


    def handle_enemy_vision_gain(self, game_object: GameObject, position: Position) -> None:
        new_watchers = self.__visibility_map.get_watching_enemies(game_object.role, position)
        for watcher in new_watchers:
            watcher.on_enemy_appear(position)


    def handle_enemy_vision_loss(self, game_object: GameObject, position: Position) -> None:
        old_watchers = self.__visibility_map.get_watching_enemies(game_object.role, position)
        for watcher in old_watchers:
            watcher.on_enemy_disappear(position)


    def handle_self_vision_gain(self, game_object: GameObject, old_vision: Set[Position],
                                new_vision: Set[Position]) -> None:

        new_vision.difference_update(old_vision)

        for position in new_vision:
            if self.is_position_occupied(position) and game_object.role.is_enemy(
                    self.__game_object_positions[position].role):
                game_object.on_enemy_appear(position)


    def handle_self_vision_loss(self, game_object: GameObject, old_vision: Set[Position],
                                new_vision: Set[Position]) -> None:

        old_vision.difference_update(new_vision)
        for position in old_vision:
            game_object.on_enemy_disappear(position)


    def handle_effect_attack(self, game_object: GameObject, effect_type: EffectType) -> None:
        effect = EffectFactory.create(effect_type)

        if effect is None:
            return

        for active_effect in game_object.active_effects:
            if active_effect.effect_type == effect.effect_type:
                self.execute_action(EffectRefreshAction(self, effect, game_object))
        else:
            self.execute_action(EffectApplyAction(self, effect, game_object))


    def handle_sight_affection(self, game_object: GameObject, old_sight: float, old_visibility: Set[Position]) -> None:
        if old_sight == game_object.get_attribute(AttributeType.SIGHT):
            return

        new_visibility = game_object.visible_tiles
        self.handle_self_vision_loss(game_object, old_visibility, new_visibility)
        self.handle_self_vision_gain(game_object, old_visibility, new_visibility)


    def execute_action(self, action: GameAction) -> None:
        action.execute()
        self.__game_history.add_action(action)


    def execute_terrain_turn(self, game_object: GameObject) -> None:
        terrain = self.__game_map[game_object.position]
        pass


    def execute_effect_turn(self, effect: Effect, owner: GameObject) -> None:
        pass


    def execute_unit_turn(self, unit: GameObject) -> None:
        pass


    def simulate_rest_of_player_turn(self, player) -> None:
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


    def apply_effect(self, game_object: GameObject, effect: Effect) -> None:
        pass


    def remove_effect(self, game_object: GameObject, effect_type: EffectType) -> None:
        pass


    def remove(self, game_object: GameObject) -> None:
        pass


    def place(self, game_object: GameObject) -> None:
        pass


    def earn(self, player: IPlayer, amount: int) -> None:
        pass


    def spend(self, player: IPlayer, amount: int) -> None:
        pass


    def create_move_action(self, game_object: GameObject, position: Position) -> None:
        pass


    def create_attack_action(self, game_object: GameObject, position: Position) -> None:
        pass


    def compute_attribute(self, game_object: GameObject, attribute_type: AttributeType, original_value: float) -> float:
        affected = self.__game_map[game_object.position].affect_attribute(attribute_type, original_value)

        for effect in game_object.active_effects:
            affected = effect.affect_attribute(attribute_type, affected)

        return affected


    def get_attribute(self, position: Position, attribute_type: AttributeType) -> float:
        if position not in self.__game_object_positions:
            return 0.0
        return self.__game_object_positions[position].get_attribute(attribute_type)


    def get_current_hit_points(self, position: Position) -> float:
        if position not in self.__game_object_positions:
            return 0.0
        return self.__game_object_positions[position].current_hit_points


    def get_attack_effect(self, position: Position) -> Set[EffectType]:
        pass


    def get_resistances(self, position: Position) -> Set[EffectType]:
        pass


    def get_active_effects(self, position: Position) -> Dict[EffectType, int]:
        pass


    def get_object_type(self, position: Position) -> GameObjectType:
        pass


    def get_role(self, position: Position) -> GameRole:
        pass


    def get_object_visible_tiles(self, game_object: GameObject) -> Set[Position]:
        return self.game_map.get_visible_tiles(self.__game_object_positions[game_object],
                                               int(game_object.get_attribute(AttributeType.SIGH)))


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


    def get_tiles_in_range(self, game_object: GameObject):
        return self.game_map.get_visible_tiles(self.__game_object_positions[game_object],
                                               int(game_object.get_attribute(AttributeType.RANGE)))


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


    @property
    def border_tiles(self) -> Set[Position]:
        pass


    def get_visible_tiles(self, position: Position, sight: int) -> Set[Position]:
        return self.__game_map.get_visible_tiles(position, sight)


    def get_accessible_tiles(self, position: Position, actions: int) -> Dict[Position, int]:
        return self.__game_map.get_accessible_tiles(position, actions)


    def spawn_unit(self, information: SpawnInformation) -> None:
        pass


    def get_resources(self, player: IPlayer) -> int:
        pass
