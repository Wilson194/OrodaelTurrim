from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Structure.Actions.Abstract import GameAction
from OrodaelTurrim.Structure.Enums import TerrainType
from OrodaelTurrim.Structure.GameObjects.GameObject import GameObject


class TerrainDamageAction(GameAction):
    def __init__(self, game_engine: GameEngine, game_object: GameObject, terrain_type: TerrainType, damage: float):
        super().__init__(game_engine)

        self.__damage = damage
        self.__terrain_type = terrain_type
        self.__game_object = game_object


    def execute(self) -> None:
        self.__game_object.take_damage(self.__damage)


    def undo(self) -> None:
        self.__game_object.receive_healing(self.__damage)


    @property
    def text(self) -> str:
        return '{} {} suffered {} damage from {} terrain tile'.format(self.__game_object.object_type,
                                                                      self.__game_object.position.offset, self.__damage,
                                                                      self.__terrain_type)
