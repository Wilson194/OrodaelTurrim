from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Structure.Enums import GameRole


class Player(IPlayer):
    def act(self) -> None:
        print('User round')


    @property
    def role(self) -> GameRole:
        return GameRole.DEFENDER


    @property
    def name(self) -> str:
        return 'Student'
