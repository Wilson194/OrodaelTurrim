from typing import TYPE_CHECKING

from OrodaelTurrim.Business.GameMap import BorderTiles
from OrodaelTurrim.Structure.Position import OffsetPosition

if TYPE_CHECKING:
    from OrodaelTurrim.Business.GameEngine import GameEngine


class SpawnUncertainty:
    def __init__(self, game_engine: "GameEngine"):
        self.__game_engine = game_engine


    def __compute_uncertainty(self):
        pass


    @property
    def spawn_information(self):
        return None
