from typing import List

from OrodaelTurrim.business.Proxy import GameObjectProxy, MapProxy
from OrodaelTurrim.structure.Enums import AttributeType, TerrainType
from OrodaelTurrim.structure.Filter.AttackFilter import AttackNearestFilter
from OrodaelTurrim.structure.Position import Position
from OrodaelTurrim.structure.Filter.FilterPattern import MoveFilter


class MoveToBaseFilter(MoveFilter):
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        bases = self.map_proxy.bases_position
        min_distance = min([x.distance_to_nearest(bases) for x in tiles])
        return [x for x in tiles if x.distance_to_nearest(bases) == min_distance]


class MoveToNearestEnemyFilter(MoveFilter):
    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy):
        super().__init__(map_proxy, game_object_proxy)

        self.__nearest_filter = AttackNearestFilter(map_proxy, game_object_proxy)


    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        enemies = self.game_object_proxy.get_visible_enemies
        if not enemies:
            return tiles

        nearest_enemies = self.__nearest_filter.filter(position, enemies)
        min_distance = min([x.distance_to_nearest(nearest_enemies) for x in tiles])

        return [x for x in tiles if x.distance_to_nearest(nearest_enemies) == min_distance]


class MoveToRangeFilter(MoveFilter):
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        enemies = self.game_object_proxy.get_visible_enemies(position).keys()
        if not enemies:
            return tiles

        attack_range = self.game_object_proxy.get_attribute(position, AttributeType.RANGE)
        return [x for x in tiles if x.distance_to_nearest(enemies) <= attack_range]


class MoveToSafeDistanceFilter(MoveFilter):
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        enemies = self.game_object_proxy.get_visible_enemies(position).keys()

        if not enemies:
            return tiles

        max_distance = max([x.distance_to_nearest(enemies) for x in tiles])
        return [x for x in tiles if x.distance_to_nearest(enemies) == max_distance]


class MoveToTerrainFilter(MoveFilter):
    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy, terrain_types: List[TerrainType]):
        super().__init__(map_proxy, game_object_proxy)
        self.__terrain_types = terrain_types


    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        return [x for x in tiles if self.map_proxy.get_terrain_type(x) in self.__terrain_types]
