from OrodaelTurrim.business.GameEngine import GameEngine
from OrodaelTurrim.structure.Actions.Abstract import GameAction
from OrodaelTurrim.structure.Enums import AttributeType
from OrodaelTurrim.structure.GameObjects.GameObject import GameObject
from OrodaelTurrim.structure.Position import Position


class AttackAction(GameAction):
    def __init__(self, game_engine: GameEngine, attacker: GameObject, target: GameObject):
        super().__init__(game_engine)

        self.__attacker = attacker
        self.__target = target

        damage = self.__attacker.get_attribute(AttributeType.ATTACK) - self.__target.get_attribute(AttributeType.DEFENSE)
        self.__damage = max(damage, 0)


    def execute(self):
        self._game_engine.damage(self.__target, self.__damage)


    def undo(self):
        self._game_engine.heal(self.__target, self.__damage)


    def __str__(self):
        return "{} [{}] attacked {} [{}] inflicting {} damage".format(self.__attacker.object_type.name,
                                                                      self.__attacker.position.offset,
                                                                      self.__target.object_type.name,
                                                                      self.__target.position.offset,
                                                                      self.__damage)


class MoveAction(GameAction):
    def __init__(self, game_engine: GameEngine, game_object: GameObject, from_position: Position, to_position: Position):
        super().__init__(game_engine)

        self.__game_object = game_object
        self.__from = from_position
        self.__to = to_position


    def execute(self):
        pass


    def undo(self):
        pass


    def __str__(self):
        pass
