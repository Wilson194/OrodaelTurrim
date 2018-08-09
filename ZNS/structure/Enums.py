from enum import Enum

from ZNS.structure.Position import Position, CubicPosition
from ZNS.structure.Terrain import Field, Forest, Hill, Mountain, River, Village


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
