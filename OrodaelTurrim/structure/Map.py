from typing import TYPE_CHECKING, List

from PyQt5.QtGui import QColor

if TYPE_CHECKING:
    from OrodaelTurrim.structure.Terrain import Terrain


class Tile:
    def __init__(self, terrain: "Terrain", border: "Border" = None):
        self.terrain = terrain
        self.border = border


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

    @staticmethod
    def full(weight: int, color: QColor):
        return Border(weight, weight, weight, weight, weight, weight, color)

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
