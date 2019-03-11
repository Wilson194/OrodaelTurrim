from typing import TYPE_CHECKING, List, Dict, Set

from PyQt5.QtGui import QColor

from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Structure.Enums import GameRole
from OrodaelTurrim.Structure.GameObjects.GameObject import GameObject
from OrodaelTurrim.Structure.Position import Position

if TYPE_CHECKING:
    pass


class Border:
    def __init__(self, right_lower: int = 0, lower: int = 0, left_lower: int = 0, left_upper: int = 0, upper: int = 0,
                 right_upper: int = 0, color: [List[QColor], QColor] = QColor(0, 0, 0)):
        self.upper = upper
        self.right_upper = right_upper
        self.right_lower = right_lower
        self.lower = lower
        self.left_lower = left_lower
        self.left_upper = left_upper
        self.__color = color


    @staticmethod
    def full(weight: int, color: QColor):
        return Border(weight, weight, weight, weight, weight, weight, color)


    @property
    def order(self):
        return [self.right_lower, self.lower, self.left_lower, self.left_upper, self.upper, self.right_upper]


    @property
    def color(self):
        if type(self.__color) is list:
            return self.__color
        else:
            return [self.__color for x in range(6)]


    @color.setter
    def color(self, value: [List[QColor], QColor]):
        self.__color = value


class VisibilityMap:
    def __init__(self):
        self.__visibility_map = {}  # type: Dict[IPlayer, Dict[Position, Set[GameObject]]]


    def register_player(self, player: IPlayer):
        self.__visibility_map[player] = {}


    def add_vision(self, game_object: GameObject, new_visible_positions: Set[Position]):
        for position in new_visible_positions:
            if position not in self.__visibility_map[game_object.owner]:
                self.__visibility_map[game_object.owner][position] = set()

            self.__visibility_map[game_object.owner][position].add(game_object)


    def remove_vision(self, game_object: GameObject, no_longer_visible: Set[Position]):
        player_map = self.__visibility_map[game_object.owner]  # type: Dict[Position,Set[GameObject]]

        for position in no_longer_visible:
            if position not in player_map:
                continue

            watcher = player_map[position]
            watcher.remove(game_object)

            if len(watcher) == 0:
                player_map.pop(position)


    def get_visible_tiles(self, player: IPlayer) -> Set[Position]:
        return set(self.__visibility_map[player].keys())


    def get_watching_enemies(self, role: GameRole, position: Position) -> List[GameObject]:
        watching_enemies = set()
        for player in self.__visibility_map.keys():
            if role.is_enemy(player.role):
                player_visibility = self.__visibility_map[player]
                if position in player_visibility:
                    watching_enemies.update(player_visibility[position])

        return list(watching_enemies)


    def clear(self):
        for player in self.__visibility_map.keys():
            self.__visibility_map[player] = {}
