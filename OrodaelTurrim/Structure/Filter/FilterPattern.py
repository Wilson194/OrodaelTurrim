import inspect
from abc import ABC, abstractmethod
from typing import List, Union
import random

from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy
from OrodaelTurrim.Structure.Position import Position
from OrodaelTurrim.Structure.Utils import Singleton


class TileFilter(ABC):
    @abstractmethod
    def filter(self, positions: Position, tiles: List[Position]):
        pass


    @staticmethod
    def use_filter(position: Position, filters: List["TileFilter"], tiles: List[Position]) -> Union[Position, None]:
        if not tiles:
            return None

        for _filter in filters:
            filtered = _filter.filter(position, tiles)

            if len(filtered) >= 1:
                tiles = filtered
                if len(filtered) == 1:
                    break

        return TileFilter.filter_random(tiles)


    @staticmethod
    def filter_random(tiles: List[Position]) -> Position:
        return random.choice(tiles)


class MoveFilter(TileFilter):

    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy):
        self.map_proxy = map_proxy  # type: MapProxy
        self.game_object_proxy = game_object_proxy  # type: GameObjectProxy


    @abstractmethod
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        pass


class AttackFilter(TileFilter):

    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy):
        self.map_proxy = map_proxy
        self.game_object_proxy = game_object_proxy


    @abstractmethod
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        pass


class FilterReference:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


