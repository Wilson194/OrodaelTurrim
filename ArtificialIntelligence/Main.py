from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Structure.Enums import GameRole, GameObjectType
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.Position import OffsetPosition


class AIPlayer(IPlayer):
    def act(self) -> None:
        print('Rigor Mortis doing his stuff')
        # try:
        #     self.game_control_proxy.spawn_unit(
        #         SpawnInformation(self, GameObjectType.GARGOYLE, OffsetPosition(5, -5), [], []))
        # except:
        #     pass


    @property
    def role(self) -> GameRole:
        return GameRole.ATTACKER


    @property
    def name(self) -> str:
        return 'Rigor Mortis'
