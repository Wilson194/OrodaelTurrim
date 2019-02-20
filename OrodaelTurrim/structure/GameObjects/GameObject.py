from typing import List, TYPE_CHECKING, Dict

from OrodaelTurrim.business.Interface import Player
from OrodaelTurrim.business.Interface.Player import IPlayer
from OrodaelTurrim.structure.Enums import AttributeType, GameObjectType, EffectType, GameRole
from OrodaelTurrim.structure.Filter.FilterPattern import TileFilter, MoveFilter, AttackFilter
from OrodaelTurrim.structure.GameObjects.Effect import Effect
from OrodaelTurrim.structure.GameObjects.Prototypes.Prototype import GameObjectPrototypePool, GameObjectPrototype
from OrodaelTurrim.structure.Position import Position

if TYPE_CHECKING:
    from OrodaelTurrim.business.GameEngine import GameEngine


class GameObject:
    def __init__(self, owner: IPlayer, position: Position, object_type: GameObjectType, game_engine: "GameEngine"):
        self.__owner = owner
        self.__game_engine = game_engine

        self.__object_type = object_type

        self.__prototype = GameObjectPrototypePool.prototypes[object_type]  # type: GameObjectPrototype
        self.__accessible_tiles = []  # type: List[Position]

        self.__move_filters = []  # type: List[MoveFilter]
        self.__attack_filters = []  # type: List[AttackFilter]

        self.__active_effects = []  # type: List[Effect]

        self.__visible_enemies = {}  # type: Dict[Position, int]
        self.__current_hit_points = self.__prototype.get_attribute_value(AttributeType.HIT_POINTS)

        self.__visible_tiles = []  # type: List[Position]
        self.__accessible_tiles = []  # type: List[Position]

        self.__position = None
        self.position = position


    def move(self) -> None:
        if self.get_attribute(AttributeType.ACTIONS) == 0 or self.__prototype.get_attribute_value(
                AttributeType.ACTIONS) == 0:
            return

        free_accessible_tiles = [x for x in self.__accessible_tiles if not self.__game_engine.is_position_occupied(x)]

        if free_accessible_tiles:
            self.__game_engine.create_move_action(self, TileFilter.use_filter(self.position, self.__move_filters,
                                                                              free_accessible_tiles))


    def attack(self) -> None:
        if self.enemies_in_range:
            self.__game_engine.create_attack_action(self, TileFilter.use_filter(self.position, self.__attack_filters,
                                                                                self.enemies_in_range))


    def recalculate_cache(self) -> None:
        self.__visible_tiles = self.__game_engine.get_visible_tiles(self.position,
                                                                    int(self.get_attribute(AttributeType.SIGHT)))

        self.__accessible_tiles = self.__game_engine.get_accessible_tiles(self.position, int(
            self.get_attribute(AttributeType.ACTIONS))).keys()


    @property
    def enemies_in_range(self):
        attack_range = int(self.get_attribute(AttributeType.RANGE))
        return [position for position, distance in self.__visible_enemies.items() if distance <= attack_range]


    def act(self):
        self.move()
        self.attack()


    def take_damage(self, damage: float) -> None:
        self.__current_hit_points -= damage


    def receive_healing(self, healing: float) -> None:
        self.__current_hit_points = min(self.__current_hit_points + healing,
                                        self.__prototype.get_attribute_value(AttributeType.HIT_POINTS))


    def apply_effect(self, effect: Effect):
        previous_sight = self.get_attribute(AttributeType.SIGHT)
        self.__active_effects.append(effect)

        if previous_sight != self.get_attribute(AttributeType.SIGHT):
            self.recalculate_cache()


    def remove_effect(self, effect_type: EffectType):
        previous_sight = self.get_attribute(AttributeType.SIGHT)
        self.__active_effects = [x for x in self.__active_effects if x.effect_type != effect_type]

        if previous_sight != self.get_attribute(AttributeType.SIGHT):
            self.recalculate_cache()


    def on_enemy_appear(self, position: Position) -> None:
        self.__visible_enemies[position] = self.position.distance_from(position)


    def on_enemy_disappear(self, position: Position) -> None:
        self.__visible_enemies.pop(position)


    def register_attack_filter(self, attack_filter: AttackFilter) -> None:
        self.__attack_filters.append(attack_filter)


    def register_move_filter(self, move_filter: MoveFilter) -> None:
        self.__move_filters.append(move_filter)


    def is_dead(self) -> bool:
        return self.__current_hit_points <= 0


    def get_attribute(self, attribute_type: AttributeType):
        return self.__game_engine.compute_attribute(self, attribute_type,
                                                    self.__prototype.get_attribute_value(attribute_type))


    @property
    def current_hit_points(self) -> float:
        return self.__current_hit_points


    @property
    def object_type(self):
        return self.__object_type


    @property
    def role(self) -> GameRole:
        return self.__prototype.role


    @property
    def owner(self) -> IPlayer:
        return self.__owner


    @property
    def position(self):
        return self.__position


    @position.setter
    def position(self, value: Position):
        self.__position = value
        self.recalculate_cache()


    @property
    def attack_effects(self):
        return self.__prototype.attack_effects


    @property
    def resistances(self):
        return self.__prototype.resistances


    @property
    def active_effects(self) -> List[Effect]:
        return self.__active_effects


    @property
    def visible_tiles(self) -> List[Position]:
        return self.__visible_tiles


    @property
    def visible_enemies(self) -> Dict[Position, int]:
        return self.__visible_enemies


class SpawnInformation:
    def __init__(self, owner: Player, object_type: GameObjectType, position: Position, attack_filters, move_filters):
        self.owner = owner
        self.object_type = object_type
        self.position = position
        self.attack_filters = attack_filters
        self.move_filters = move_filters
