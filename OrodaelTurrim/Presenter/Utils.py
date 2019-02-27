from OrodaelTurrim import IMAGES_ROOT
from OrodaelTurrim.Structure.Enums import GameObjectType, TerrainType


class GetMeta(type):
    def __getitem__(self, item):
        return AssetsEncoder.assets[item]


class AssetsEncoder(metaclass=GetMeta):
    assets = {
        GameObjectType.ARCHER: IMAGES_ROOT / 'Objects' / 'archer.png',
        GameObjectType.BASE: IMAGES_ROOT / 'Objects' / 'base.png',
        GameObjectType.DRUID: IMAGES_ROOT / 'Objects' / 'druid.png',
        GameObjectType.ENT: IMAGES_ROOT / 'Objects' / 'ent.png',
        GameObjectType.KNIGHT: IMAGES_ROOT / 'Objects' / 'knight.png',
        GameObjectType.MAGICIAN: IMAGES_ROOT / 'Objects' / 'magician.png',

        GameObjectType.CYCLOPS: IMAGES_ROOT / 'Objects' / 'cyclops.png',
        GameObjectType.DEMON: IMAGES_ROOT / 'Objects' / 'demon.png',
        GameObjectType.ELEMENTAL: IMAGES_ROOT / 'Objects' / 'elemental.png',
        GameObjectType.GARGOYLE: IMAGES_ROOT / 'Objects' / 'gargoyle.png',
        GameObjectType.MINOTAUR: IMAGES_ROOT / 'Objects' / 'minotaur.png',
        GameObjectType.NECROMANCER: IMAGES_ROOT / 'Objects' / 'necromancer.png',
        GameObjectType.ORC: IMAGES_ROOT / 'Objects' / 'orc.png',
        GameObjectType.SKELETON: IMAGES_ROOT / 'Objects' / 'skeleton.png',

        TerrainType.FIELD: IMAGES_ROOT / 'Terrain' / 'field.png',
        TerrainType.FOREST: IMAGES_ROOT / 'Terrain' / 'forest.png',
        TerrainType.HILL: IMAGES_ROOT / 'Terrain' / 'hill.png',
        TerrainType.MOUNTAIN: IMAGES_ROOT / 'Terrain' / 'mountain.png',
        TerrainType.RIVER: IMAGES_ROOT / 'Terrain' / 'river_0-2.png',
        TerrainType.VILLAGE: IMAGES_ROOT / 'Terrain' / 'village.png',

        'river_0-2': IMAGES_ROOT / 'Terrain' / 'river_0-2.png',
        'river_0-3': IMAGES_ROOT / 'Terrain' / 'river_0-3.png',
        'river_0-4': IMAGES_ROOT / 'Terrain' / 'river_0-4.png',
        'river_1-3': IMAGES_ROOT / 'Terrain' / 'river_1-3.png',
        'river_1-4': IMAGES_ROOT / 'Terrain' / 'river_1-4.png',
        'river_1-5': IMAGES_ROOT / 'Terrain' / 'river_1-5.png',
        'river_2-4': IMAGES_ROOT / 'Terrain' / 'river_2-4.png',
        'river_2-5': IMAGES_ROOT / 'Terrain' / 'river_2-5.png',
        'river_3-5': IMAGES_ROOT / 'Terrain' / 'river_3-5.png',

        'river_2-3': IMAGES_ROOT / 'Terrain' / 'river_2-4.png',
        'river_0-5': IMAGES_ROOT / 'Terrain' / 'river_0-3.png',
        'river_3-4': IMAGES_ROOT / 'Terrain' / 'river_3-5.png',
    }