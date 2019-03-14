from typing import List, Set

from OrodaelTurrim.Structure.GameObjects.Attributes import AttributeBundle
from OrodaelTurrim.Structure.Enums import EffectType, GameObjectType, GameRole
from OrodaelTurrim.Structure.GameObjects.Prototypes.Prototype import GameObjectPrototype


class Cyclops(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(20, 10, 80, 2, 2, 3)
    COST = 60
    ASSET_NAME = "cyclops"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.BURN}


class Demon(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(25, 5, 150, 2, 3, 3)
    COST = 80
    ASSET_NAME = "demon"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return {EffectType.BURN}


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.BURN, EffectType.FREEZE}


class Elemental(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(10, 10, 60, 3, 2, 3)
    COST = 35
    ASSET_NAME = "elemental"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return {EffectType.BURN}


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.BURN}


class Gargoyle(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(5, 10, 60, 3, 1, 5)
    COST = 30
    ASSET_NAME = "gargoyle"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.FREEZE}


class Minotaur(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(10, 20, 150, 2, 1, 2)
    COST = 50
    ASSET_NAME = "minotaur"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.ROOT}


class Necromancer(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(20, 5, 75, 3, 2, 3)
    COST = 50
    ASSET_NAME = "necromancer"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.ROOT}


class Orc(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(8, 5, 35, 2, 1, 3)
    COST = 8
    ASSET_NAME = "orc"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.ROOT}


class Skeleton(GameObjectPrototype):
    ATTRIBUTES = AttributeBundle(5, 2, 20, 2, 1, 2)
    COST = 5
    ASSET_NAME = "skeleton"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.BLIND}
