from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from OrodaelTurrim.structure.Enums import TerrainType


class Terrain(ABC):
    @abstractmethod
    def get_move_cost(self, target: 'TerrainType') -> int:
        pass


    @abstractmethod
    def get_remaining_sigh(self, current_sight: int) -> int:
        pass


    @abstractmethod
    def affect_attribute(self, attribute, original_value: float) -> float:
        pass


    @property
    @abstractmethod
    def terrain_type(self) -> 'TerrainType':
        pass


    def info_text(self):
        return ""


class Field(Terrain):
    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 3
        elif target in (TerrainType.HILL, TerrainType.FOREST, TerrainType.RIVER):
            return 2
        else:
            return 1


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight - 1


    def affect_attribute(self, attribute, original_value: float) -> float:
        raise NotImplemented


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.structure.Enums import TerrainType
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
        from OrodaelTurrim.structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 3
        elif target in (TerrainType.HILL, TerrainType.RIVER):
            return 2
        else:
            return 1


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight - 3


    def affect_attribute(self, attribute, original_value: float) -> float:
        raise NotImplemented


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.structure.Enums import TerrainType
        return TerrainType.FOREST


    def char(self) -> str:
        return 'F'


class Hill(Terrain):
    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.structure.Enums import TerrainType
        if target == TerrainType.HILL:
            return 1
        else:
            return 2


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight // 2


    def affect_attribute(self, attribute, original_value: float) -> float:
        raise NotImplemented


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.structure.Enums import TerrainType
        return TerrainType.HILL


    def char(self) -> str:
        return 'H'


class Mountain(Terrain):
    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 2
        else:
            return 3


    def get_remaining_sigh(self, current_sight: int) -> int:
        return 0


    def affect_attribute(self, attribute, original_value: float) -> float:
        raise NotImplemented


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.structure.Enums import TerrainType
        return TerrainType.MOUNTAIN


    def char(self) -> str:
        return 'M'


class River(Terrain):
    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.structure.Enums import TerrainType
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


    def affect_attribute(self, attribute, original_value: float) -> float:
        raise NotImplemented


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.structure.Enums import TerrainType
        return TerrainType.RIVER


    def char(self) -> str:
        return 'R'


class Village(Terrain):
    def get_move_cost(self, target: 'Terrain') -> int:
        from OrodaelTurrim.structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 3
        elif target in (TerrainType.FOREST, TerrainType.HILL, TerrainType.RIVER):
            return 2
        else:
            return 1


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight - 1


    def affect_attribute(self, attribute, original_value: float) -> float:
        raise NotImplemented


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.structure.Enums import TerrainType
        return TerrainType.VILLAGE


    def char(self) -> str:
        return 'V'
