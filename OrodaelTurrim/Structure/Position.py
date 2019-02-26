from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING, Union, Set
import math

from PyQt5.QtCore import QPointF, QPoint
from PyQt5.QtGui import QColor

if TYPE_CHECKING:
    from OrodaelTurrim.Structure.Enums import Nudge, HexDirection


class Point(QPointF):
    def __init__(self, x, y):
        super().__init__(x, y)


    @property
    def x(self):
        return super().x()


    @property
    def y(self):
        return super().y()


    @property
    def QPointF(self):
        return QPointF(super().x(), super().y())


    def __add__(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y)


    def __mul__(self, other: [float, int, 'Point']) -> 'Point':
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        else:
            return Point(self.x * other, self.y * other)


    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


class Position(ABC):
    # Correction for aligning along X axis
    CORRECTION_X = 1e-6

    # Correction for aligning along Y axis
    CORRECTION_Y = 2e-6

    # Correction for aligning along Z axis
    CORRECTION_Z = -3e-6


    def __init__(self):
        pass


    @property
    @abstractmethod
    def cubic(self) -> 'CubicPosition':
        pass


    @property
    @abstractmethod
    def axial(self) -> 'AxialPosition':
        pass


    @property
    @abstractmethod
    def offset(self) -> 'OffsetPosition':
        pass


    @property
    @abstractmethod
    def int_coord(self) -> 'Position':
        pass


    def __sub__(self, other: 'Position') -> 'Position':
        return CubicPosition(self.cubic.x - other.cubic.x, self.cubic.y - other.cubic.y, self.cubic.z - other.cubic.z)


    def __add__(self, other: 'Position') -> 'Position':
        return CubicPosition(self.cubic.x + other.cubic.x, self.cubic.y + other.cubic.y, self.cubic.z + other.cubic.z)


    def length(self):
        return (abs(self.cubic.x) + abs(self.cubic.y) + abs(self.cubic.z)) // 2


    def interpolate(self, start: float, finish: float, progress: float) -> float:
        return start + (finish - start) * progress


    def interpolate_to(self, position: 'Position', progress: float, nudge: 'Nudge') -> 'Position':
        x = self.interpolate(self.cubic.x + nudge.nudge(Position.CORRECTION_X),
                             position.cubic.x + nudge.nudge(Position.CORRECTION_X), progress)
        y = self.interpolate(self.cubic.y + nudge.nudge(Position.CORRECTION_Y),
                             position.cubic.y + nudge.nudge(Position.CORRECTION_Y), progress)
        z = self.interpolate(self.cubic.z + nudge.nudge(Position.CORRECTION_Z),
                             position.cubic.z + nudge.nudge(Position.CORRECTION_Z), progress)
        return CubicPosition(x, y, z)


    def distance_from(self, position: 'Position') -> int:
        return (self - position).length()


    def distance_to_nearest(self, positions: List['Position']) -> int:
        return min([self.distance_from(x) for x in positions])


    def neighbour(self, direction: 'HexDirection') -> 'Position':
        return self + CubicPosition(direction.value.cubic.x, direction.value.cubic.y, direction.value.cubic.z)


    def get_all_neighbours(self) -> List['Position']:
        from OrodaelTurrim.Structure.Enums import HexDirection
        return [self.neighbour(x) for x in
                [HexDirection.UPPER, HexDirection.RIGHT_UPPER, HexDirection.RIGHT_LOWER, HexDirection.LOWER,
                 HexDirection.LEFT_LOWER, HexDirection.LEFT_UPPER] if self.neighbour(x)]


    def plot_line(self, position: 'Position', nudge: 'Nudge') -> List['Position']:
        distance = self.distance_from(position)

        step = 1.0 / max(distance, 1)
        line = list()

        for i in range(distance + 1):
            line.append(self.interpolate_to(position, step * i, nudge))

        return line


    @staticmethod
    def from_pixel(point: Union[QPoint, Point, QPointF], transformation: float) -> "AxialPosition":
        from OrodaelTurrim.Presenter.Widgets.Map import HEXAGON_SIZE

        x_size = (HEXAGON_SIZE.x * transformation / 2)
        y_size = (HEXAGON_SIZE.y * transformation / math.sqrt(3))

        q = (2 / 3 * point.x()) / x_size
        r = ((-1 / 3 * point.x()) / x_size) + ((math.sqrt(3) / 3 * point.y()) / y_size)

        return AxialPosition(q, r).int_coord


class CubicPosition(Position):
    __slots__ = ['__x_position', '__y_position', '__z_position']


    def __init__(self, x_position, y_position, z_position):
        super().__init__()

        self.__x_position = x_position
        self.__y_position = y_position
        self.__z_position = z_position


    @property
    def cubic(self) -> 'CubicPosition':
        return self


    @property
    def axial(self) -> 'AxialPosition':
        return AxialPosition(self.__x_position, self.__z_position)


    @property
    def offset(self) -> 'OffsetPosition':
        col = self.__x_position
        row = self.__z_position + (self.__x_position - (abs(self.__x_position) % 2)) // 2
        return OffsetPosition(col, row)


    @property
    def x(self):
        return self.__x_position


    @property
    def y(self):
        return self.__y_position


    @property
    def z(self):
        return self.__z_position


    def __eq__(self, other: 'CubicPosition'):
        return self.x == other.cubic.x and self.y == other.cubic.y and self.z == other.cubic.z


    def __hash__(self):
        return hash((self.offset.q, self.offset.r))


    def __lt__(self, other):
        return self.x < other.cubic.x if self.x != other.cubic.x else self.y < other.cubic.y if self.y != other.cubic.y else self.z < other.z


    @property
    def int_coord(self):
        rx = int(round(self.__x_position))
        ry = int(round(self.__y_position))
        rz = int(round(self.__z_position))

        x_diff = abs(rx - self.__x_position)
        y_diff = abs(ry - self.__y_position)
        z_diff = abs(rz - self.__z_position)

        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry

        return CubicPosition(rx, ry, rz)


    def __repr__(self):
        return '<Cubic> {}, {}, {}'.format(self.x, self.y, self.z)


class AxialPosition(Position):
    __slots__ = ['__q', '__r']


    def __init__(self, q: Union[int, float], r: Union[int, float]):
        super().__init__()

        self.__q = q
        self.__r = r


    @property
    def cubic(self) -> 'CubicPosition':
        return CubicPosition(self.__q, -self.__q - self.__r, self.__r)


    @property
    def axial(self) -> 'AxialPosition':
        return self


    @property
    def offset(self) -> 'OffsetPosition':
        return self.cubic.offset


    @property
    def q(self):
        return self.__q


    @property
    def r(self):
        return self.__r


    @property
    def int_coord(self) -> "AxialPosition":
        p = self.cubic.int_coord.axial
        return AxialPosition(p.q, p.r)


    def __eq__(self, other: 'AxialPosition') -> bool:
        return self.q == other.q and self.r == other.r


    def __hash__(self):
        return hash((self.offset.q, self.offset.r))


    def __repr__(self):
        return '<Axial> {}, {}'.format(self.q, self.r)


class OffsetPosition(Position):
    __slots__ = ['__q', '__r']


    def __init__(self, q: int, r: int):
        super().__init__()
        self.__q = q
        self.__r = r


    @property
    def cubic(self) -> 'CubicPosition':
        x = self.__q
        z = self.__r - (self.__q - (self.__q & 1)) // 2
        y = -x - z
        return CubicPosition(x, y, z)


    @property
    def axial(self) -> 'AxialPosition':
        return self.cubic.axial


    @property
    def offset(self) -> 'OffsetPosition':
        return self


    @property
    def q(self):
        return self.__q


    @property
    def r(self):
        return self.__r


    def __eq__(self, other: 'OffsetPosition'):
        return self.q == other.offset.q and self.r == other.offset.r


    def __hash__(self):
        return hash((self.offset.q, self.offset.r))


    def __lt__(self, other):
        if self.q == other.q:
            return self.r < other.q

        return self.q < other.q


    @property
    def int_coord(self):
        p = self.cubic.int_coord.offset
        return OffsetPosition(p.q, p.r)


    def __repr__(self):
        return '<Offset> {}, {}'.format(self.q, self.r)
