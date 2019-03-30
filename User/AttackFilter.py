from typing import List

from OrodaelTurrim.Structure.Filter.FilterPattern import AttackFilter
from OrodaelTurrim.Structure.Position import Position


class DummyAttackFilter(AttackFilter):
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        return tiles
