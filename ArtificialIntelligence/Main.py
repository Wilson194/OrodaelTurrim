from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Structure.Enums import GameRole


class AIPlayer(IPlayer):
    def act(self) -> None:
        print('Rigor Mortis doing his stuff')


    @property
    def role(self) -> GameRole:
        return GameRole.ATTACKER


    @property
    def name(self) -> str:
        return 'Rigor Mortis'
