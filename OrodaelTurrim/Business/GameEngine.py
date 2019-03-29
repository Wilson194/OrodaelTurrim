import copy
import time
from typing import List, Dict, Set

from PyQt5.QtCore import pyqtSignal, QRunnable, pyqtSlot
from antlr4 import *

from OrodaelTurrim.Business.Factory import EffectFactory
from OrodaelTurrim.Business.History import GameHistory
from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Business.Uncertainty import SpawnUncertainty
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Structure.Actions.Abstract import GameAction
from OrodaelTurrim.Structure.Actions.Combat import MoveAction, AttackAction
from OrodaelTurrim.Structure.Actions.Effect import EffectRefreshAction, EffectApplyAction, EffectTickAction, \
    EffectDamageAction, EffectExpireAction
from OrodaelTurrim.Structure.Actions.Placement import DieAction, SpawnAction
from OrodaelTurrim.Structure.Actions.Resources import EarnResourcesAction, SpendResourcesAction
from OrodaelTurrim.Structure.Actions.Terrain import TerrainDamageAction
from OrodaelTurrim.Structure.Exceptions import IllegalActionException
from OrodaelTurrim.Structure.GameObjects.Effect import Effect
from OrodaelTurrim.Structure.GameObjects.Prototypes.Prototype import GameObjectPrototypePool
from OrodaelTurrim.Structure.Map import VisibilityMap
from OrodaelTurrim.Structure.Resources import PlayerResources
from OrodaelTurrim.Business.GameMap import GameMap
from OrodaelTurrim.Structure.Enums import AttributeType, GameObjectType, TerrainType, EffectType, GameRole
from OrodaelTurrim.Structure.GameObjects.GameObject import GameObject, SpawnInformation, UncertaintySpawn
from OrodaelTurrim.Structure.Position import Position
from OrodaelTurrim.Structure.TypeStrucutre import TwoWayDict


class GameEngine:

    def __init__(self, game_map: GameMap):
        GameEngine.__new__ = lambda x: print('Cannot create GameEngine instance')
        self.__remaining_turns = None
        self.__game_map = game_map
        self.__players = []  # type: List[IPlayer]
        self.__player_resources = {}  # type: Dict[IPlayer, PlayerResources]
        self.__player_units = {}  # type: Dict[IPlayer, List[GameObject]]

        self.__defender_bases = {}  # type: Dict[IPlayer, GameObject]

        self.__game_object_positions = {}  # type: Dict[Position,GameObject]

        self.__game_history = None  # type: GameHistory

        self.__turn_limit = None  # type: int
        self.__initial_resources = {}  # type: Dict[IPlayer, PlayerResources]

        self.__visibility_map = VisibilityMap()

        self.__spawn_uncertainty = SpawnUncertainty(self)


    def start(self, turn_limit: int) -> None:
        self.__turn_limit = turn_limit
        self.__game_history = GameHistory(turn_limit, self.__players)


    def restart(self):
        self.__game_history = GameHistory(self.__turn_limit + self.__game_history.turns_count, self.__players)
        self.__player_resources = {key: value for key, value in self.__initial_resources.items()}

        for player in self.__player_units.keys():
            self.__player_units[player] = []
        self.__defender_bases = {}
        self.__game_object_positions = {}

        self.__visibility_map.clear()

        self.__spawn_uncertainty.clear()

        # Connector().emit('redraw_ui')
        # Connector().emit('redraw_map')


    def register_player(self, player: IPlayer, resources: PlayerResources,
                        unit_spawn_info: List[SpawnInformation]) -> None:
        self.__players.append(player)
        self.__player_resources[player] = resources
        self.__player_units[player] = []

        self.__initial_resources[player] = copy.deepcopy(resources)

        self.__visibility_map.register_player(player)
        if player.role == GameRole.ATTACKER:
            self.__spawn_uncertainty.register_attacker(player)

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

        self.__visibility_map.add_vision(game_object, game_object.visible_tiles)

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

        gain_vision = copy.deepcopy(new_vision)
        gain_vision.difference_update(old_vision)

        for position in gain_vision:
            if self.is_position_occupied(position) and game_object.role.is_enemy(
                    self.__game_object_positions[position].role):
                game_object.on_enemy_appear(position)


    def handle_self_vision_loss(self, game_object: GameObject, old_vision: Set[Position],
                                new_vision: Set[Position]) -> None:

        lost_vision = copy.deepcopy(old_vision)
        lost_vision.difference_update(new_vision)
        for position in lost_vision:
            game_object.on_enemy_disappear(position)


    def handle_effect_attack(self, game_object: GameObject, effect_type: EffectType) -> None:
        effect = EffectFactory.create(effect_type)

        if effect is None:
            return

        for active_effect in game_object.active_effects:
            if active_effect.effect_type == effect.effect_type:
                self.execute_action(EffectRefreshAction(self, active_effect, game_object))
                break
        else:
            self.execute_action(EffectApplyAction(self, effect, game_object))


    def handle_sight_affection(self, game_object: GameObject, old_sight: float, old_visibility: Set[Position]) -> None:
        if old_sight == game_object.get_attribute(AttributeType.SIGHT):
            return

        new_visibility = game_object.visible_tiles

        # Update visibility map
        vision_lost = old_visibility - new_visibility
        vision_gain = new_visibility - old_visibility
        self.__visibility_map.remove_vision(game_object, vision_lost)
        self.__visibility_map.add_vision(game_object, vision_gain)

        self.handle_self_vision_loss(game_object, old_visibility, new_visibility)
        self.handle_self_vision_gain(game_object, old_visibility, new_visibility)


    def execute_action(self, action: GameAction) -> None:
        if self.__game_history.in_preset:
            self.__game_history.add_action(action)
        action.execute()


    def execute_terrain_turn(self, game_object: GameObject) -> None:
        terrain = self.__game_map[game_object.position]
        potential_damage = terrain.compute_damage(game_object.current_hit_points)

        if potential_damage != 0:
            self.execute_action(TerrainDamageAction(self, game_object, terrain.terrain_type, potential_damage))


    def execute_effect_turn(self, effect: Effect, owner: GameObject) -> None:
        self.execute_action(EffectTickAction(self, effect, owner))

        potential_damage = effect.compute_damage(owner.current_hit_points)
        if potential_damage != 0:
            self.execute_action(EffectDamageAction(self, effect, owner, potential_damage))

        if effect.hax_expired:
            self.execute_action(EffectExpireAction(self, effect, owner))


    def execute_unit_turn(self, unit: GameObject) -> None:
        self.execute_terrain_turn(unit)

        effects = unit.active_effects
        for effect in effects:
            self.execute_effect_turn(effect, unit)

        if not unit.is_dead():
            unit.act()


    def simulate_rest_of_player_turn(self, player) -> None:
        units = self.__player_units[player]

        for unit in units:
            if Connector().get_variable('game_over'):
                return
            self.execute_unit_turn(unit)

        income = self.__player_resources[player].income
        self.execute_action(EarnResourcesAction(self, player, income))

        # Check base
        if player.role == GameRole.DEFENDER and self.__game_history.in_preset and not self.player_have_base(player):
            Connector().emit('game_over')
            return

        self.__game_history.end_turn()


    def damage(self, game_object: GameObject, damage: float):
        game_object.take_damage(damage)
        if game_object.is_dead() and self.get_game_history().in_preset:
            self.execute_action(DieAction(self, game_object))


    def heal(self, game_object: GameObject, amount: float) -> None:
        game_object.receive_healing(amount)


    def move(self, game_object: GameObject, to: Position) -> None:
        position_from = game_object.position

        del self.__game_object_positions[position_from]
        self.__game_object_positions[to] = game_object

        old_visibility = game_object.visible_tiles
        game_object.position = to
        new_visibility = game_object.visible_tiles

        # Update visibility map
        vision_lost = old_visibility - new_visibility
        vision_gain = new_visibility - old_visibility
        self.__visibility_map.remove_vision(game_object, vision_lost)
        self.__visibility_map.add_vision(game_object, vision_gain)

        self.handle_self_vision_loss(game_object, old_visibility, new_visibility)
        self.handle_self_vision_gain(game_object, old_visibility, new_visibility)

        self.handle_enemy_vision_loss(game_object, position_from)
        self.handle_enemy_vision_gain(game_object, to)


    def apply_effect(self, game_object: GameObject, effect: Effect) -> None:
        old_sight = game_object.get_attribute(AttributeType.SIGHT)
        old_visibility = game_object.visible_tiles

        game_object.apply_effect(effect)
        self.handle_sight_affection(game_object, old_sight, old_visibility)


    def remove_effect(self, game_object: GameObject, effect_type: EffectType) -> None:
        old_sight = game_object.get_attribute(AttributeType.SIGHT)
        old_visibility = game_object.visible_tiles

        game_object.remove_effect(effect_type)

        self.handle_sight_affection(game_object, old_sight, old_visibility)


    def remove(self, game_object: GameObject) -> None:
        if game_object.object_type == GameObjectType.BASE:
            for player, _game_object in self.__defender_bases.items():
                if game_object == _game_object:
                    del self.__defender_bases[player]

                    if self.__game_history.in_preset and not Connector().get_variable('game_over'):
                        Connector().set_variable('game_over', True)
                        Connector().emit('game_over')
                    break

        self.delete_game_object(game_object)


    def place(self, game_object: GameObject) -> None:
        self.register_game_object(game_object)


    def earn(self, player: IPlayer, amount: int) -> None:
        self.__player_resources[player].add_resources(amount)
        Connector().emit('redraw_ui')


    def spend(self, player: IPlayer, amount: int) -> None:
        self.__player_resources[player].remove_resources(amount)
        Connector().emit('redraw_ui')


    def create_move_action(self, game_object: GameObject, position: Position) -> None:
        if game_object is not None and position is not None:
            self.execute_action(MoveAction(self, game_object, game_object.position, position))


    def create_attack_action(self, game_object: GameObject, position: Position) -> None:
        if game_object is None or position is None or not position in self.__game_object_positions:
            return

        attacked = self.__game_object_positions[position]
        self.execute_action(AttackAction(self, game_object, attacked))

        attack_effects = copy.deepcopy(game_object.attack_effects)
        attack_effects.difference_update(attacked.resistances)

        for effect_type in attack_effects:
            self.handle_effect_attack(attacked, effect_type)


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
        if position not in self.__game_object_positions:
            return set()

        return self.__game_object_positions[position].attack_effects


    def get_resistances(self, position: Position) -> Set[EffectType]:
        if position not in self.__game_object_positions:
            return set()

        return self.__game_object_positions[position].resistances


    def get_active_effects(self, position: Position) -> Dict[EffectType, int]:
        active_effects = {}
        if position not in self.__game_object_positions:
            return active_effects

        effects = self.__game_object_positions[position].active_effects
        for effect in effects:
            active_effects[effect.effect_type] = effect.remaining_duration

        return active_effects


    def get_object_type(self, position: Position) -> GameObjectType:
        if position not in self.__game_object_positions:
            return GameObjectType.NONE

        return self.__game_object_positions[position].object_type


    def get_role(self, position: Position) -> GameRole:
        if position not in self.__game_object_positions:
            return GameRole.NEUTRAL

        return self.__game_object_positions[position].role


    def get_visible_tiles(self, position: Position) -> Set[Position]:
        if position not in self.__game_object_positions:
            return set()

        return self.__game_object_positions[position].visible_tiles


    def get_visible_enemies(self, position: Position) -> Dict[Position, int]:
        if position not in self.__game_object_positions:
            return dict()

        return self.__game_object_positions[position].visible_enemies


    def get_map_height(self) -> int:
        return self.__game_map.size[1]


    def get_map_width(self) -> int:
        return self.__game_map.size[0]


    def get_terrain_type(self, position: Position) -> TerrainType:
        return self.__game_map[position].terrain_type


    def is_position_on_map(self, position: Position) -> bool:
        return self.__game_map.position_on_map(position)


    def is_position_occupied(self, position: Position) -> bool:
        return position in self.__game_object_positions


    def get_bases_positions(self) -> Set[Position]:
        """
        Test documentation
        :return:
        """
        return set([x.position for x in self.__defender_bases.values()])


    def get_border_tiles(self) -> Set[Position]:
        return self.__game_map.border_tiles


    def get_player_visible_tiles(self, player: IPlayer) -> Set[Position]:
        return self.__visibility_map.get_visible_tiles(player)


    def get_object_visible_tiles(self, position: Position, sight: int) -> Set[Position]:
        return self.__game_map.get_visible_tiles(position, sight)


    def get_accessible_tiles(self, position: Position, actions: int) -> Dict[Position, int]:
        return self.__game_map.get_accessible_tiles(position, actions)


    def spawn_unit(self, information: SpawnInformation) -> None:
        prototype = GameObjectPrototypePool[information.object_type]

        resources = self.__player_resources[information.owner].resources

        if information.object_type == GameObjectType.BASE and information.owner in self.__defender_bases:
            raise IllegalActionException('You cannot spawn additional base!')

        if resources < prototype.cost:
            raise IllegalActionException('Insufficient resources!')

        if not self.is_position_on_map(information.position):
            raise IllegalActionException('Position is not on the map!')

        if self.is_position_occupied(information.position):
            raise IllegalActionException('Tile is already occupied!')

        if information.owner.role != prototype.role:
            raise IllegalActionException('Attempt to spawn unit of different role!')

        self.execute_action(SpendResourcesAction(self, information.owner, prototype.cost))
        self.execute_action(SpawnAction(self, self.create_unit(information)))

        self.unit_spawn_signal()


    def get_resources(self, player: IPlayer) -> int:
        return self.__player_resources[player].resources


    def get_income(self, player: IPlayer) -> int:
        return self.__player_resources[player].income


    def get_game_map(self):
        return self.__game_map


    def set_game_map(self, value):
        self.__game_map = value


    def get_game_object(self, position: Position) -> GameObject:
        return self.__game_object_positions[position]


    def get_player(self, player_index: int) -> IPlayer:
        return self.__players[player_index]


    def get_game_history(self) -> GameHistory:
        return self.__game_history


    def player_have_base(self, player: IPlayer) -> bool:
        return player in self.__defender_bases


    def unit_spawn_signal(self):
        pass
        # Connector().emit('redraw_map')
        # Connector().emit('redraw_ui')


    def spawn_information(self) -> List[List[UncertaintySpawn]]:
        return self.__spawn_uncertainty.spawn_information


    def run_game_rounds(self, rounds: int, display: bool) -> None:
        game_history = self.get_game_history()
        while rounds > 0 and not Connector().get_variable('game_over'):
            time.sleep(0)
            game_history.active_player.act()
            self.simulate_rest_of_player_turn(game_history.active_player)

            if display and game_history.on_first_player:
                Connector().emit('redraw_map')

            if game_history.on_first_player:
                rounds -= 1
