from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from OrodaelTurrim import IMAGES_ROOT
from OrodaelTurrim.structure.Attributes import AttributeBundle
from OrodaelTurrim.structure.Enums import GameObjectType, GameRole, AttributeType, EffectType
from OrodaelTurrim.structure.GameObjects.Prototypes.Attackers import Cyclops, Demon, Elemental, Gargoyle, Minotaur, Necromancer, \
    Orc, Skeleton
from OrodaelTurrim.structure.GameObjects.Prototypes.Defenders import Base, Archer, Druid, Ent, Knight, Magician


class GameObjectPrototype(ABC):
    ASSET_FORMAT = '.png'
    ASSET_FOLDER = IMAGES_ROOT / 'Objects'


    def __init__(self, attributes: AttributeBundle, cost: int, object_type: GameObjectType, role: GameRole, asset_name: str):
        self.__attributes = attributes
        self.__cost = cost
        self.__object_type = object_type
        self.__role = role
        self.__asset_name = asset_name


    def get_attribute_value(self, attribute_type: AttributeType) -> float:
        try:
            return getattr(self.__attributes, attribute_type.name.capitalize())
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


    @abstractmethod
    @property
    def attack_effects(self) -> List[EffectType]:
        pass


    @abstractmethod
    @property
    def resistances(self) -> List[EffectType]:
        pass


class GameObjectPrototypePool:
    prototypes = {
        GameObjectType.BASE, Base(),
        GameObjectType.ARCHER, Archer(),
        GameObjectType.DRUID, Druid(),
        GameObjectType.ENT, Ent(),
        GameObjectType.KNIGHT, Knight(),
        GameObjectType.MAGICIAN, Magician(),

        GameObjectType.CYCLOPS, Cyclops(),
        GameObjectType.DEMON, Demon(),
        GameObjectType.ELEMENTAL, Elemental(),
        GameObjectType.GARGOYLE, Gargoyle(),
        GameObjectType.MINOTAUR, Minotaur(),
        GameObjectType.NECROMANCER, Necromancer(),
        GameObjectType.ORC, Orc(),
        GameObjectType.SKELETON, Skeleton()
    }
