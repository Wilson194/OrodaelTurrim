from typing import Union, List, TYPE_CHECKING, Set

from PyQt5.QtGui import QColor

from OrodaelTurrim.Structure.Enums import EffectType, HexDirection
from OrodaelTurrim.Structure.GameObjects.Effect import Burn, Blind, Freeze, Root, Effect
from OrodaelTurrim.Structure.Map import Border

if TYPE_CHECKING:
    from OrodaelTurrim.Structure.Position import Position


class EffectFactory:
    @staticmethod
    def create(effect_type: EffectType) -> Union[Effect, None]:
        if effect_type == EffectType.BURN:
            return Burn()

        elif effect_type == EffectType.BLIND:
            return Blind()

        elif effect_type == EffectType.FREEZE:
            return Freeze()

        elif effect_type == EffectType.ROOT:
            return Root()

        else:
            return None


class BorderFactory:
    @staticmethod
    def create(weight: int, color: QColor, positions: Set["Position"]):
        borders_dict = {}
        for position in positions:
            directions = {}
            for direction in HexDirection.direction_list():
                if position.cubic + direction.value not in positions:
                    directions[direction.name.lower()] = weight
            directions['color'] = color
            borders_dict[position] = Border(**directions)

        return borders_dict



