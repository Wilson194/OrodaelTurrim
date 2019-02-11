from typing import List

from OrodaelTurrim.structure.Attributes import AttributeBundle
from OrodaelTurrim.structure.Enums import AttributeType, EffectType, GameObjectType


class GameObject:
    def __init__(self, attributes: AttributeBundle, game_object_type: GameObjectType):
        self.__actions = attributes.actions
        self.__move_range = attributes.move_range
        self.__sight = attributes.sight

        self.__attack = attributes.attack
        self.__defense = attributes.defense
        self.__hit_points = attributes.hit_points

        self.__game_object_type = game_object_type
        self.__attack_filters = []

        self.__resistances = []
        self.__attack_effects = []

    def act(self) -> None:
        pass

    def get_attribute(self, attribute: AttributeType) -> float:
        pass

    def get_attack_effects(self) -> List[EffectType]:
        pass

    def get_resistances(self) -> List[EffectType]:
        pass

    def get_type(self) -> GameObjectType:
        return self.__game_object_type
