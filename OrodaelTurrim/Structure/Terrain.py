from abc import ABC, abstractmethod

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from OrodaelTurrim.Structure.Enums import TerrainType, AttributeType


class Terrain(ABC):
    def compute_damage(self, hit_points: float) -> float:
        return 0


    def affect_actions(self, original_value: float) -> float:
        return original_value


    def affect_max_hit_points(self, original_value: int) -> int:
        return original_value


    def affect_range(self, original_value: int) -> int:
        return original_value


    def affect_sight(self, original_value: int) -> int:
        return original_value


    def affect_attack(self, original_value: float) -> float:
        return original_value


    def affect_defense(self, original_value: float) -> float:
        return original_value


    def affect_attribute(self, attribute: "AttributeType", original_value: Union[int, float]) -> Union[float, int]:
        if attribute == AttributeType.ACTIONS:
            return self.affect_actions(original_value)

        elif attribute == AttributeType.HIT_POINTS:
            return self.affect_max_hit_points(original_value)

        elif attribute == AttributeType.RANGE:
            return self.affect_range(original_value)

        elif attribute == AttributeType.SIGHT:
            return self.affect_sight(original_value)

        elif attribute == AttributeType.ATTACK:
            return self.affect_attack(original_value)

        elif attribute == AttributeType.DEFENSE:
            return self.affect_defense(original_value)


    @abstractmethod
    def get_move_cost(self, target: 'TerrainType') -> int:
        pass


    @abstractmethod
    def get_remaining_sigh(self, current_sight: int) -> int:
        pass


    @property
    @abstractmethod
    def terrain_type(self) -> 'TerrainType':
        pass


    def info_text(self):
        return ""


class Field(Terrain):
    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 3
        elif target in (TerrainType.HILL, TerrainType.FOREST, TerrainType.RIVER):
            return 2
        else:
            return 1


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight - 1


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.FIELD


    def char(self) -> str:
        return 'I'


    def info_text(self):
        return """    
        <br>            
        <h3>Beautiful field</h3>
        """.format()


class Forest(Terrain):
    def get_move_cost(self, target: 'Terrain') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 3
        elif target in (TerrainType.HILL, TerrainType.RIVER):
            return 2
        else:
            return 1


    def affect_attack(self, original_value: float):  # TODO: Check value of multiplier
        return original_value * 0.2


    def affect_defense(self, original_value: float):
        return original_value * 0.1


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight - 3


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.FOREST


    def char(self) -> str:
        return 'F'


class Hill(Terrain):
    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.HILL:
            return 1
        else:
            return 2


    def affect_attack(self, original_value: float):
        return original_value * 0.1


    def affect_defense(self, original_value: float):
        return original_value * 0.1


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight // 2


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.HILL


    def char(self) -> str:
        return 'H'


class Mountain(Terrain):
    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 2
        else:
            return 3


    def affect_attack(self, original_value: float):
        return original_value * -0.2


    def affect_defense(self, original_value: float):
        return original_value * 0.5


    def affect_sight(self, original_value: int):
        return original_value + 3


    def get_remaining_sigh(self, current_sight: int) -> int:
        return 0


    def compute_damage(self, hit_points: float):
        return hit_points * 0.05


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.MOUNTAIN


    def char(self) -> str:
        return 'M'


class River(Terrain):
    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 4
        elif target in (TerrainType.FOREST, TerrainType.HILL):
            return 3
        elif target == TerrainType.RIVER:
            return 1
        else:
            return 2


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight - 1


    def affect_attack(self, original_value: float):
        return original_value * -0.2


    def affect_defense(self, original_value: float):
        return original_value * -0.2


    def affect_actions(self, original_value: float):
        return original_value - 1


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.RIVER


    def char(self) -> str:
        return 'R'


class Village(Terrain):
    def get_move_cost(self, target: 'Terrain') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 3
        elif target in (TerrainType.FOREST, TerrainType.HILL, TerrainType.RIVER):
            return 2
        else:
            return 1


    def affect_attack(self, original_value: float):
        return original_value * 0


    def affect_defense(self, original_value: float):
        return original_value * 0.3


    def affect_actions(self, original_value: float):
        return original_value + 1


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight - 1


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.VILLAGE


    def char(self) -> str:
        return 'V'
