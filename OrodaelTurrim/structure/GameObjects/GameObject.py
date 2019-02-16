from abc import ABC
from typing import List, TYPE_CHECKING

from OrodaelTurrim.business.Interface import Player
from OrodaelTurrim.business.Interface.Player import IPlayer
from OrodaelTurrim.structure.Attributes import AttributeBundle
from OrodaelTurrim.structure.Enums import AttributeType, EffectType, GameObjectType
from OrodaelTurrim.structure.GameObjects.Prototypes.Prototype import GameObjectPrototypePool, GameObjectPrototype
from OrodaelTurrim.structure.Position import Position

if TYPE_CHECKING:
    from OrodaelTurrim.business.GameEngine import GameEngine


class GameObject:
    def __init__(self, owner: IPlayer, position: Position, object_type: GameObjectType, game_engine: GameEngine):
        self.__owner = owner
        self.__game_engine = game_engine

        self.__object_type = object_type

        self.__prototype = GameObjectPrototypePool.prototypes[object_type]  # type: GameObjectPrototype
        self.__accessible_tiles = []  # type: List[Position]

        self.__position = None
        self.position = position


    def move(self):
        if self.get_attribute(AttributeType.ACTIONS) == 0 or self.__prototype.get_attribute_value(AttributeType.ACTIONS) == 0:
            return

        accessible_tiles = [x for x in self.__accessible_tiles if not self.__game_engine.is_position_occupied(x)]

        if accessible_tiles:
            pass


    def attack(self):
        pass


    def recalculate_cache(self):
        pass


    def get_enemies_in_range(self):
        pass


    def act(self):
        self.move()
        self.attack()


    def take_damage(self, damage: float) -> None:
        pass


    def receive_healing(self, healing: float) -> None:
        pass


    def apply_effect(self, effect):
        pass


    def remove_effect(self, effect):
        pass


    def on_move(self, position: Position):
        pass


    def on_enemy_appear(self, position: Position):
        pass


    def on_enemy_disappear(self, position: Position):
        pass


    def register_attack_filter(self, attack_filter):
        pass


    def register_move_filter(self, move_filter):
        pass


    @property
    def position(self):
        return self.__position


    @position.setter
    def position(self, value: Position):
        self.__position = value
        self.recalculate_cache()


    @property
    def object_type(self):
        return self.__object_type


    def get_attribute(self, attribute_type: AttributeType):
        return self.__game_engine.compute_attribute(self, attribute_type, self.__prototype.get_attribute_value(attribute_type))


class SpawnInformation:
    def __init__(self, owner: Player, object_type: GameObjectType, position: Position, attack_filters, move_filters):
        self.owner = owner
        self.object_type = object_type
        self.position = position
        self.attack_filters = attack_filters
        self.move_filters = move_filters
