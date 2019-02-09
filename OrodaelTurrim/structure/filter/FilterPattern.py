import sys
from abc import ABC, abstractmethod
from typing import List

from OrodaelTurrim.business.Interface.Accessor import GameObjectAccessor, MapTileAccessor
from OrodaelTurrim.structure.GameObject import GameObject
from OrodaelTurrim.structure.Position import Position


class TileFilter(ABC):
    @abstractmethod
    def filter(self, positions: List[Position]):
        pass


class MoveFilter(TileFilter):
    def __init__(self, owner: GameObject, game_object_accessor: GameObjectAccessor, map_tile_accessor: MapTileAccessor):
        self._owner = owner
        self._game_object_accessor = game_object_accessor
        self._map_tile_accessor = map_tile_accessor


    @abstractmethod
    def filter(self, positions: List[Position]) -> List[Position]:
        pass


    def distance_to_nearest_enemy(self, position: Position, enemies: List[Position]) -> int:
        return min([position.distance_from(enemy) for enemy in enemies])


    def get_visible_enemies(self, free_tiles: List[Position]) -> List[Position]:
        occupied_tiles = self._map_tile_accessor
        return []


class AttackFilter(TileFilter):
    @abstractmethod
    def filter(self, positions: List[Position]) -> List[Position]:
        pass
