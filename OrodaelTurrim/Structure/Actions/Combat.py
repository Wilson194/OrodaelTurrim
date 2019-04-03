from OrodaelTurrim.Structure.Actions.Abstract import GameAction
from OrodaelTurrim.Structure.Enums import AttributeType
from OrodaelTurrim.Structure.GameObjects.GameObject import GameObject
from OrodaelTurrim.Structure.Position import Position
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from OrodaelTurrim.Business.GameEngine import GameEngine


class AttackAction(GameAction):
    """  Represents game action of one game object attacking another """


    def __init__(self, game_engine: "GameEngine", attacker: GameObject, target: GameObject):
        super().__init__(game_engine)

        self.__attacker = attacker
        self.__target = target

        damage = self.__attacker.get_attribute(AttributeType.ATTACK) - self.__target.get_attribute(
            AttributeType.DEFENSE)
        self.__damage = max(damage, 0)


    def execute(self) -> None:
        self._game_engine.damage(self.__target, self.__damage)


    def undo(self) -> None:
        self._game_engine.heal(self.__target, self.__damage)


    @property
    def text(self) -> str:
        return "{} [{}] attacked {} [{}] inflicting {} damage".format(self.__attacker.object_type.name,
                                                                      self.__attacker.position.offset,
                                                                      self.__target.object_type.name,
                                                                      self.__target.position.offset,
                                                                      self.__damage)


class MoveAction(GameAction):
    """ Represents game action of game object moving """


    def __init__(self, game_engine: "GameEngine", game_object: GameObject, from_position: Position,
                 to_position: Position):
        super().__init__(game_engine)

        self.__game_object = game_object
        self.__from = from_position
        self.__to = to_position


    def execute(self) -> None:
        self._game_engine.move(self.__game_object, self.__to)


    def undo(self) -> None:
        self._game_engine.move(self.__game_object, self.__from)


    @property
    def text(self) -> str:
        return '{} moved: {} -> {}'.format(str(self.__game_object.object_type), self.__from.offset, self.__to.offset)
