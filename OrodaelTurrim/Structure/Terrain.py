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
        from OrodaelTurrim.Structure.Enums import AttributeType

        if attribute == AttributeType.ACTIONS:
            return self.affect_actions(original_value)

        elif attribute == AttributeType.HIT_POINTS:
            return self.affect_max_hit_points(original_value)

        elif attribute == AttributeType.ATTACK_RANGE:
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
        <p>Sight cost: 1</p>        
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
        return original_value * 1.2


    def affect_defense(self, original_value: float):
        return original_value * 1.1


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight - 3


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.FOREST


    def char(self) -> str:
        return 'F'


    def info_text(self):
        return """    
        <br>            
        <p>Sight cost: 3</p>        
        <p>Attack bonus: 0.2</p>        
        <p>Defence bonus: 0.1</p>        
        """.format()


class Hill(Terrain):
    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.HILL:
            return 1
        else:
            return 2


    def affect_attack(self, original_value: float):
        return original_value * 1.1


    def affect_defense(self, original_value: float):
        return original_value * 1.1


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight // 2


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.HILL


    def char(self) -> str:
        return 'H'


    def info_text(self):
        return """    
        <br>            
        <p>Sight cost: half</p>        
        <p>Attack bonus: 0.1</p>        
        <p>Defence bonus: 0.1</p>        
        """.format()


class Mountain(Terrain):
    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 2
        else:
            return 3


    def affect_attack(self, original_value: float):
        return original_value * 0.8


    def affect_defense(self, original_value: float):
        return original_value * 1.5


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

    def info_text(self):
        return """    
        <br>            
        <p>Sight cost: all</p>        
        <p>Attack bonus: -0.2</p>        
        <p>Defence bonus: 0.5</p>        
        <p>Damage: 0.05</p>        
        """.format()



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
        return original_value * 0.8


    def affect_defense(self, original_value: float):
        return original_value * 0.8


    def affect_actions(self, original_value: float):
        return original_value - 1


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.RIVER


    def char(self) -> str:
        return 'R'

    def info_text(self):
        return """    
        <br>            
        <p>Sight cost: 1</p>        
        <p>Attack bonus: -0.2</p>        
        <p>Action reduction: 1</p>        
        <p>Defence bonus: -0.2</p>        
        """.format()



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
        return original_value * 1


    def affect_defense(self, original_value: float):
        return original_value * 1.3


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

    def info_text(self):
        return """    
        <br>            
        <p>Sight cost: 1</p>        
        <p>Attack bonus: 0</p>        
        <p>Defence bonus: 0.3</p>        
        <p>Actions bonus: 1</p>        
        """.format()

