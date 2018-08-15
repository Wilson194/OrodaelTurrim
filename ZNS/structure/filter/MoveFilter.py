import sys
from typing import List

from ZNS.structure.Enums import AttributeType
from ZNS.structure.Position import Position
from ZNS.structure.filter.FilterPattern import MoveFilter


class MoveToBaseFilter(MoveFilter):

    def filter(self, positions: List[Position]) -> List[Position]:
        bases = self._map_tile_accessor.get_bases_positions()

        filtered = []

        min_distance = sys.maxsize

        for position in positions:
            distance = self.distance_to_nearest_enemy(position, bases)
            if distance <= min_distance and distance != 0:
                if distance < min_distance:
                    min_distance = distance
                    filtered.clear()

                filtered.append(position)

        return filtered


class MoveToNearestFilter(MoveFilter):
    def filter(self, positions: List[Position]) -> List[Position]:
        pass


class MoveToRangeFilter(MoveFilter):
    def filter(self, positions: List[Position]) -> List[Position]:
        enemies = self.get_visible_enemies(positions)

        if not enemies:
            return positions

        move_range = self._owner.get_attribute(AttributeType.RANGE)
