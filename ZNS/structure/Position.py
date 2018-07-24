from abc import ABC, abstractmethod
from math import sqrt, tan, radians
from typing import List

from PyQt5.QtCore import QPoint, QPointF
from PyQt5.QtGui import QColor


class Point(QPointF):
    def __init__(self, x, y):
        super().__init__(x, y)


    @property
    def x(self):
        return super().x()


    @property
    def y(self):
        return super().y()


    def __add__(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y)


    def __mul__(self, other: [float, int]):
        return Point(self.x * other, self.y * other)


    @property
    def QPointF(self):
        return QPointF(self.x, self.y)


class Position(ABC):
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


class CubicPosition(Position):
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
        row = self.__z_position + (self.__x_position - (self.__x_position & 1)) // 2
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
        print(other.x, other.y, other.z)
        return self.x == other.x and self.y == other.y and self.z == other.z


    def __repr__(self):
        return '<Cubic> {}, {}, {}'.format(self.x, self.y, self.z)


class AxialPosition(Position):
    def __init__(self, q: int, r):
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


    def __eq__(self, other: 'AxialPosition') -> bool:
        return self.q == other.q and self.r == other.r


    def __repr__(self):
        return '<Axial> {}, {}'.format(self.q, self.r)


class OffsetPosition(Position):
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
        return self.q == other.q and self.r == other.r


    def __repr__(self):
        return '<Offset> {}, {}'.format(self.q, self.r)


class Border:
    def __init__(self, right_lower: int = 0, lower: int = 0, left_lower: int = 0, left_upper: int = 0, upper: int = 0,
                 right_upper: int = 0, color: [List[QColor], QColor] = QColor(0, 0, 0)):
        self.upper = upper
        self.right_upper = right_upper
        self.right_lower = right_lower
        self.lower = lower
        self.left_lower = left_lower
        self.left_upper = left_upper
        self.__color = color


    @property
    def order(self):
        return [self.right_lower, self.lower, self.left_lower, self.left_upper, self.upper, self.right_upper]


    @property
    def color(self):
        if type(self.__color) is list:
            return self.__color
        else:
            return [self.__color for x in range(6)]


    @color.setter
    def color(self, value: [List[QColor], QColor]):
        self.__color = value
