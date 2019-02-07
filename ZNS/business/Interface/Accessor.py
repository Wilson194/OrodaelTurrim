from typing import List

from ZNS.business.GameEngine import GameEngine
from ZNS.structure.GameObject import GameObject
from ZNS.structure.Position import Position


class GameObjectAccessor:
    def __init__(self, game_engine: GameEngine):
        self.__game_engine = game_engine


class MapTileAccessor:
    def __init__(self, game_engine: GameEngine):
        self.__game_engine = game_engine

    def get_bases_positions(self) -> List[Position]:
        return self.__game_engine.get_bases_positions()

    def get_visible_tiles(self, game_object: GameObject) -> List[Position]:
        return self.__game_engine.get_visible_tiles(game_object)

    def get_tiles_in_range(self, game_object: GameObject) -> List[Position]:
        return self.__game_engine.get_tiles_in_range(game_object)
