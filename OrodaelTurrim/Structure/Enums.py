from enum import Enum
from typing import List

from OrodaelTurrim.Structure.Position import Position, CubicPosition
from OrodaelTurrim.Structure.Terrain import Field, Forest, Hill, Mountain, River, Village


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
    ATTACK_RANGE = ()
    SIGHT = ()


class GameRole(AutoNumber):
    ATTACKER = ()
    DEFENDER = ()
    NEUTRAL = ()


    def is_enemy(self, role: "GameRole"):
        if self == role or self == GameRole.NEUTRAL or role == GameRole.NEUTRAL:
            return False
        return True


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


    @staticmethod
    def defenders() -> List["GameObjectType"]:
        return [x for x in list(GameObjectType) if x.value[0] == GameRole.DEFENDER]


    @staticmethod
    def attackers() -> List["GameObjectType"]:
        return [x for x in list(GameObjectType) if x.value[0] == GameRole.ATTACKER]


    @property
    def price(self) -> int:
        return self.value[1]


    @property
    def role(self) -> GameRole:
        return self.value[0]


class GameOverStates(AutoNumber):
    FIND_REASON = ()
    TRY_AGAIN = ()
    LET_HIM_DIE = ()
