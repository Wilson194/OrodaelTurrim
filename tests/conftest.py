from typing import List

import pytest

from ZNS.business.GameMap import GameMap
from ZNS.structure.Enums import TerrainType
from ZNS.structure.Position import Position


@pytest.fixture
def game_map() -> GameMap:
    tiles = [
        [TerrainType.RIVER, TerrainType.FIELD, TerrainType.FIELD, TerrainType.FOREST, TerrainType.VILLAGE],
        [TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.MOUNTAIN],
        [TerrainType.FOREST, TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.FIELD, TerrainType.RIVER],
        [TerrainType.VILLAGE, TerrainType.MOUNTAIN, TerrainType.HILL, TerrainType.HILL, TerrainType.HILL],
        [TerrainType.RIVER, TerrainType.FIELD, TerrainType.FOREST, TerrainType.FIELD, TerrainType.FOREST],
    ]

    return GameMap(5, 5, tiles)


@pytest.fixture
def utils():
    return Utils()


class Utils:
    def compare_position_list(self, list1: List[Position], list2: List[Position]) -> bool:
        list1 = [x.offset for x in list1]
        list2 = [x.offset for x in list2]
        list1.sort()
        list2.sort()

        return len(set(list1) - set(list2)) == 0 and len(set(list2) - set(list1)) == 0
