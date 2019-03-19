from typing import TYPE_CHECKING, List

from OrodaelTurrim.Business.GameMap import BorderTiles
from OrodaelTurrim.Business.Interface.Player import IAttacker
from OrodaelTurrim.Structure.GameObjects.GameObject import UncertaintySpawn
from OrodaelTurrim.Structure.Position import OffsetPosition

if TYPE_CHECKING:
    from OrodaelTurrim.Business.GameEngine import GameEngine


class SpawnUncertainty:
    def __init__(self, game_engine: "GameEngine"):
        self.__attackers = []
        self.__spawn_uncertainty = {}
        self.__game_engine = game_engine


    def register_attacker(self, attacker: IAttacker):
        self.__attackers.append(attacker)


    def __compute_uncertainty(self, _round: int):
        current_turn = self.__game_engine.get_game_history().current_turn

        for attacker in self.__attackers:
            spawns = attacker.spawn_information_list[_round - current_turn - 1]

            self.__spawn_uncertainty[_round] = []
            for spawn in spawns:
                self.__spawn_uncertainty[_round].append(UncertaintySpawn(spawn.position, 1.0, spawn.object_type, 1.0))


    @property
    def spawn_information(self) -> List[List[UncertaintySpawn]]:
        current_turn = self.__game_engine.get_game_history().current_turn
        for _round in range(1, 4):
            if current_turn + _round not in self.__spawn_uncertainty:
                self.__compute_uncertainty(current_turn + _round)

        return [self.__spawn_uncertainty[x] for x in range(current_turn + 1, current_turn + 4)]
