from abc import ABC
from typing import List

from OrodaelTurrim.business.Interface import Player
from OrodaelTurrim.business.Interface.Player import IPlayer
from OrodaelTurrim.structure.Attributes import AttributeBundle
from OrodaelTurrim.structure.Enums import AttributeType, EffectType, GameObjectType
from OrodaelTurrim.structure.Position import Position


class GameObject(ABC):
    def __init__(self, owner: IPlayer, attributes: AttributeBundle, game_object_type: GameObjectType):
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

        self.__owner = owner

    def act(self) -> None:
        pass

    def get_attribute(self, attribute: AttributeType) -> float:
        pass

    def get_attack_effects(self) -> List[EffectType]:
        pass

    def get_resistances(self) -> List[EffectType]:
        pass

    @property
    def object_type(self) -> GameObjectType:
        return self.__game_object_type

    @property
    def owner(self) -> IPlayer:
        return self.__owner


class SpawnInformation:
    def __init__(self, owner: Player, object_type: GameObjectType, position: Position, attack_filters, move_filters):
        self.owner = owner
        self.object_type = object_type
        self.position = position
        self.attack_filters = attack_filters
        self.move_filters = move_filters
