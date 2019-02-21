from typing import List

from OrodaelTurrim.Structure.GameObjects.Attributes import AttributeBundle
from OrodaelTurrim.Structure.Enums import GameRole, GameObjectType, EffectType
from OrodaelTurrim.Structure.GameObjects.Prototypes.Prototype import GameObjectPrototype


class Archer(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(10, 5, 50, 3, 4)
    COST = 5
    ASSET_NAME = "archer"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> List[EffectType]:
        return []


    @property
    def resistances(self) -> List[EffectType]:
        return [EffectType.BLIND]


class Base(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(5, 0, 500, 1, 2)
    COST = 0
    ASSET_NAME = "base"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> List[EffectType]:
        return []


    @property
    def resistances(self) -> List[EffectType]:
        return [EffectType.BLIND]


class Druid(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(30, 10, 100, 2, 6)
    COST = 25
    ASSET_NAME = "druid"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> List[EffectType]:
        return [EffectType.FREEZE]


    @property
    def resistances(self) -> List[EffectType]:
        return []


class Ent(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(10, 50, 200, 1, 2)
    COST = 50
    ASSET_NAME = "ent"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> List[EffectType]:
        return [EffectType.ROOT]


    @property
    def resistances(self) -> List[EffectType]:
        return [EffectType.FREEZE]


class Knight(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(20, 20, 100, 1, 2)
    COST = 10
    ASSET_NAME = "knight"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> List[EffectType]:
        return [EffectType.BLIND]


    @property
    def resistances(self) -> List[EffectType]:
        return [EffectType.ROOT]


class Magician(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(50, 5, 75, 2, 3)
    COST = 30
    ASSET_NAME = "magician"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> List[EffectType]:
        return [EffectType.BURN]


    @property
    def resistances(self) -> List[EffectType]:
        return [EffectType.BURN]
