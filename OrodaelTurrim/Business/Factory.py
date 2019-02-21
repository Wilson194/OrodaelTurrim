from typing import Union

from OrodaelTurrim.Structure.Enums import EffectType
from OrodaelTurrim.Structure.GameObjects.Effect import Burn, Blind, Freeze, Root, Effect


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
