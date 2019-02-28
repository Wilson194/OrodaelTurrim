from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Set

from OrodaelTurrim import IMAGES_ROOT
from OrodaelTurrim.Structure.GameObjects.Attributes import AttributeBundle
from OrodaelTurrim.Structure.Enums import GameObjectType, GameRole, AttributeType, EffectType


class GameObjectPrototype(ABC):
    ASSET_FORMAT = '.png'
    ASSET_FOLDER = IMAGES_ROOT / 'Objects'


    def __init__(self, attributes: AttributeBundle, cost: int, object_type: GameObjectType, role: GameRole,
                 asset_name: str):
        self.__attributes = attributes
        self.__cost = cost
        self.__object_type = object_type
        self.__role = role
        self.__asset_name = asset_name


    def get_attribute_value(self, attribute_type: AttributeType) -> float:
        try:
            return getattr(self.__attributes, attribute_type.name.lower())
        except AttributeError:
            print('Unknown type of attribute - {}!'.format(attribute_type))
            return 0.0


    @property
    def cost(self) -> int:
        return self.__cost


    @property
    def object_type(self) -> GameObjectType:
        return self.__object_type


    @property
    def role(self) -> GameRole:
        return self.__role


    @property
    def path(self) -> Path:
        return self.ASSET_FOLDER / (self.__asset_name + self.ASSET_FORMAT)


    @property
    @abstractmethod
    def attack_effects(self) -> Set[EffectType]:
        pass


    @property
    @abstractmethod
    def resistances(self) -> List[EffectType]:
        pass


    @property
    def description(self) -> str:
        return '''Actions: {} <br>
        Attack: {}<br>        
        Defense: {}<br>
        Attack range: {}<br>
        Sight: {} <br>
        Hit points: {} / {{}}'''.format(self.get_attribute_value(AttributeType.ACTIONS),
                                      self.get_attribute_value(AttributeType.ATTACK),
                                      self.get_attribute_value(AttributeType.DEFENSE),
                                      self.get_attribute_value(AttributeType.ATTACK_RANGE),
                                      self.get_attribute_value(AttributeType.SIGHT),
                                      self.get_attribute_value(AttributeType.HIT_POINTS),
                                      )


class GetMeta(type):
    def __getitem__(self, item):
        return GameObjectPrototypePool.prototypes[item]


class GameObjectPrototypePool(metaclass=GetMeta):
    from OrodaelTurrim.Structure.GameObjects.Prototypes.Attackers import Cyclops, Demon, Elemental, Gargoyle, \
        Minotaur, Necromancer, Orc, Skeleton
    from OrodaelTurrim.Structure.GameObjects.Prototypes.Defenders import Base, Archer, Druid, Ent, Knight, Magician
    prototypes = {
        GameObjectType.BASE: Base(),
        GameObjectType.ARCHER: Archer(),
        GameObjectType.DRUID: Druid(),
        GameObjectType.ENT: Ent(),
        GameObjectType.KNIGHT: Knight(),
        GameObjectType.MAGICIAN: Magician(),

        GameObjectType.CYCLOPS: Cyclops(),
        GameObjectType.DEMON: Demon(),
        GameObjectType.ELEMENTAL: Elemental(),
        GameObjectType.GARGOYLE: Gargoyle(),
        GameObjectType.MINOTAUR: Minotaur(),
        GameObjectType.NECROMANCER: Necromancer(),
        GameObjectType.ORC: Orc(),
        GameObjectType.SKELETON: Skeleton()
    }
