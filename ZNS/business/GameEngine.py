from typing import List

from ZNS.business.GameMap import GameMap
from ZNS.structure.Enums import AttributeType
from ZNS.structure.GameObject import GameObject
from ZNS.structure.Position import Position
from ZNS.structure.TypeStrucutre import TwoWayDict


class GameEngine:
    def __init__(self, turns, game_map: GameMap):
        self.__remaining_turns = turns
        self.__game_map = game_map
        self.__players = []
        self.__player_resources = {}
        self.__player_incomes = {}
        self.__player_units = {}
        self.__defender_bases = {}
        self.__game_object_hit_points = {}
        self.__game_object_effects = {}
        self.__game_object_positions = TwoWayDict()


    @property
    def game_map(self):
        return self.__game_map


    @game_map.setter
    def game_map(self, value):
        self.__game_map = value


    def get_bases_positions(self) -> List[Position]:
        positions = []

        for base in self.__defender_bases:
            positions.append(self.__game_object_positions[base])

        return positions


    def get_visible_tiles(self, game_object: GameObject):
        return self.game_map.get_visible_tiles(self.__game_object_positions[game_object],
                                               int(game_object.get_attribute(AttributeType.SIGH)))


    def get_tiles_in_range(self, game_object: GameObject):
        return self.game_map.get_visible_tiles(self.__game_object_positions[game_object],
                                               int(game_object.get_attribute(AttributeType.RANGE)))
