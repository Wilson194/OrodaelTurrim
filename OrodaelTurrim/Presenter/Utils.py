from OrodaelTurrim import IMAGES_ROOT
from OrodaelTurrim.Structure.Enums import GameObjectType


class GetMeta(type):
    def __getitem__(self, item):
        return AssetsEncoder.assets[item]


class AssetsEncoder(metaclass=GetMeta):
    assets = {
        GameObjectType.ARCHER: IMAGES_ROOT / 'Objects' / 'archer.png',
        GameObjectType.BASE: IMAGES_ROOT / 'Objects' / 'base.png',
        GameObjectType.DRUID: IMAGES_ROOT / 'Objects' / 'druid.png',
        GameObjectType.ENT: IMAGES_ROOT / 'Objects' / 'ent.png',
    }
