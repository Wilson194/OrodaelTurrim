from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Structure.Actions.Abstract import GameAction
from OrodaelTurrim.Structure.GameObjects.Effect import Effect
from OrodaelTurrim.Structure.GameObjects.GameObject import GameObject


class EffectApplyAction(GameAction):
    def __init__(self, game_engine: GameEngine, effect: Effect, owner: GameObject):
        super().__init__(game_engine)
        self.__effect = effect
        self.__owner = owner


    def execute(self) -> None:
        self._game_engine.apply_effect(self.__owner, self.__effect)


    def undo(self) -> None:
        self._game_engine.remove_effect(self.__owner, self.__effect.effect_type)


    @property
    def text(self) -> str:
        return '{} effect has been attached to {} {}'.format(self.__effect.effect_type, self.__owner.object_type,
                                                             self.__owner.position.offset)


class EffectDamageAction(GameAction):
    def __init__(self, game_engine: GameEngine, effect: Effect, owner: GameObject, damage: float):
        super().__init__(game_engine)

        self.__effect = effect
        self.__owner = owner
        self.__damage = damage


    def execute(self) -> None:
        self._game_engine.damage(self.__owner, self.__damage)


    def undo(self) -> None:
        self._game_engine.heal(self.__owner, self.__damage)


    @property
    def text(self) -> str:
        return '{} {} suffered {} damage from {}'.format(self.__owner.object_type, self.__owner.position.offset,
                                                         self.__damage, self.__effect.effect_type)


class EffectExpireAction(GameAction):
    def __init__(self, game_engine: GameEngine, effect: Effect, owner: GameObject):
        super().__init__(game_engine)

        self.__effect = effect
        self.__owner = owner


    def execute(self) -> None:
        self._game_engine.remove_effect(self.__owner, self.__effect.effect_type)


    def undo(self) -> None:
        self._game_engine.apply_effect(self.__owner, self.__effect)


    @property
    def text(self) -> str:
        return '{} effect attached to {} {} has expired'.format(self.__effect.effect_type, self.__owner.object_type,
                                                                self.__owner.position.offset)


class EffectRefreshAction(GameAction):
    def __init__(self, game_engine: GameEngine, effect: Effect, owner: GameObject):
        super().__init__(game_engine)

        self.__effect = effect
        self.__owner = owner

        self.__previous_remaining_duration = effect.remaining_duration


    def execute(self) -> None:
        self.__effect.refresh()


    def undo(self) -> None:
        self.__effect.remaining_duration = self.__previous_remaining_duration


    @property
    def text(self) -> str:
        return '{} effect attached to {} {} has been refreshed'.format(self.__effect.effect_type,
                                                                       self.__owner.object_type,
                                                                       self.__owner.position.offset)


class EffectTickAction(GameAction):
    def __init__(self, game_engine: GameEngine, effect: Effect, owner: GameObject):
        super().__init__(game_engine)
        self.__effect = effect
        self.__owner = owner

        self.__remaining_duration = self.__effect.remaining_duration - 1


    def execute(self) -> None:
        self.__effect.tick()


    def undo(self) -> None:
        self.__effect.un_tick()


    @property
    def text(self) -> str:
        return '{} effect attached to {} {} has ticked (remaining duration: {})'.format(self.__effect.effect_type,
                                                                                        self.__owner.object_type,
                                                                                        self.__owner.position.offset,
                                                                                        self.__remaining_duration)
