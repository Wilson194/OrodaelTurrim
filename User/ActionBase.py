from ExpertSystem.Business.UserFramework import IActionBase
from OrodaelTurrim.Structure.Enums import GameObjectType
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.Position import OffsetPosition


class ActionBase(IActionBase):
    def build_base(self, position_q: int, position_r: int):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player, GameObjectType.BASE, OffsetPosition(position_q, position_r), [], []))
