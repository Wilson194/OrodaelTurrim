from abc import ABC, abstractmethod

from ZNS.structure.Enums import TerrainType


class Terrain(ABC):
    @abstractmethod
    def get_move_cost(self, target: 'Terrain') -> int:
        pass


    @abstractmethod
    def get_remaining_sigh(self, current_sight: int) -> int:
        pass


    @abstractmethod
    def affect_attribute(self, attribute, original_value: float) -> float:
        pass


    @abstractmethod
    def get_type(self) -> TerrainType:
        pass


class Field(Terrain):
    def get_move_cost(self, target: TerrainType) -> int:
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


    def get_type(self) -> TerrainType:
        return TerrainType.FIELD


class Forest(Terrain):
    def get_move_cost(self, target: 'Terrain') -> int:
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


    def get_type(self) -> TerrainType:
        return TerrainType.FOREST


class Hill(Terrain):
    def get_move_cost(self, target: TerrainType) -> int:
        if target == TerrainType.HILL:
            return 1
        else:
            return 2


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight // 2


    def affect_attribute(self, attribute, original_value: float) -> float:
        raise NotImplemented


    def get_type(self) -> TerrainType:
        return TerrainType.HILL


class Mountain(Terrain):
    def get_move_cost(self, target: TerrainType) -> int:
        if target == TerrainType.MOUNTAIN:
            return 2
        else:
            return 3


    def get_remaining_sigh(self, current_sight: int) -> int:
        return 0


    def affect_attribute(self, attribute, original_value: float) -> float:
        raise NotImplemented


    def get_type(self) -> TerrainType:
        return TerrainType.MOUNTAIN


class River(Terrain):
    def get_move_cost(self, target: TerrainType) -> int:
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


    def get_type(self) -> TerrainType:
        return TerrainType.RIVER


class Village(Terrain):
    def get_move_cost(self, target: 'Terrain') -> int:
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


    def get_type(self) -> TerrainType:
        return TerrainType.VILLAGE
