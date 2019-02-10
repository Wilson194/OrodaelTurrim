from enum import Enum

from OrodaelTurrim.structure.Position import Position, CubicPosition
from OrodaelTurrim.structure.Terrain import Field, Forest, Hill, Mountain, River, Village


class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class TerrainType(Enum):
    FIELD = Field()
    FOREST = Forest()
    HILL = Hill()
    MOUNTAIN = Mountain()
    RIVER = River()
    VILLAGE = Village()


class Nudge(Enum):
    POSITIVE = 1
    NEGATIVE = -1

    def nudge(self, value: float) -> float:
        return self.value * value


class HexDirection(Enum):
    UPPER = CubicPosition(0, 1, -1)
    RIGHT_UPPER = CubicPosition(1, 0, -1)
    RIGHT_LOWER = CubicPosition(1, -1, 0)
    LOWER = CubicPosition(0, -1, 1)
    LEFT_LOWER = CubicPosition(-1, 0, 1)
    LEFT_UPPER = CubicPosition(-1, 1, 0)


class EffectType(AutoNumber):
    BLIND = ()
    BURN = ()
    FREEZE = ()
    ROOT = ()


class AttributeType(AutoNumber):
    ACTIONS = ()
    ATTACK = ()
    DEFENSE = ()
    HIT_POINTS = ()
    RANGE = ()
    SIGH = ()


class GameRole(AutoNumber):
    ATTACKER = ()
    DEFENDER = ()
    NEUTRAL = ()


class GameObjectType(Enum):
    NONE = (GameRole.NEUTRAL, 0)
    BASE = (GameRole.DEFENDER, 0)

    ARCHER = (GameRole.DEFENDER, 5)
    DRUID = (GameRole.DEFENDER, 25)
    ENT = (GameRole.DEFENDER, 50)
    KNIGHT = (GameRole.DEFENDER, 10)
    MAGICIAN = (GameRole.DEFENDER, 30)

    CYCLOPS = (GameRole.ATTACKER, 60)
    DEMON = (GameRole.ATTACKER, 80)
    ELEMENTAL = (GameRole.ATTACKER, 35)
    GARGOYLE = (GameRole.ATTACKER, 30)
    MINOTAUR = (GameRole.ATTACKER, 50)
    NECROMANCER = (GameRole.ATTACKER, 50)
    ORC = (GameRole.ATTACKER, 8)
    SKELETON = (GameRole.ATTACKER, 5)
