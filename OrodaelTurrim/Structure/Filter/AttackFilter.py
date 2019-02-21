from typing import List

from OrodaelTurrim.Structure.Enums import GameObjectType, AttributeType
from OrodaelTurrim.Structure.Filter.FilterPattern import AttackFilter
from OrodaelTurrim.Structure.Position import Position


class AttackBaseFilter(AttackFilter):
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        return [x for x in tiles if self.game_object_proxy.get_type(position) == GameObjectType.BASE]


class AttackLeastVisibleFilter(AttackFilter):
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        min_hit_points = min([self.game_object_proxy.get_current_hit_points(x) for x in tiles])
        return [x for x in tiles if self.game_object_proxy.get_current_hit_points(x) == min_hit_points]


class AttackMostVulnerableFilter(AttackFilter):
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        min_defence = min([self.game_object_proxy.get_attribute(x, AttributeType.DEFENSE) for x in tiles])
        return [x for x in tiles if self.game_object_proxy.get_attribute(x, AttributeType.DEFENSE) == min_defence]


class AttackNearestFilter(AttackFilter):
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        min_distance = min([x.distance_from(position) for x in tiles])
        return [x for x in tiles if x.distance_from(position) == min_distance]


class AttackNoResistantFilter(AttackFilter):
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        attack_effect = self.game_object_proxy.get_attack_effects(position)
        if not attack_effect:
            return tiles

        filtered = []
        for tile in tiles:
            resistances = self.game_object_proxy.get_resistances(tile)
            if not all([x in attack_effect for x in resistances]):
                filtered.append(tile)

        return filtered


class AttackStrongestFilter(AttackFilter):
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        max_attack = max([self.game_object_proxy.get_attribute(x, AttributeType.ATTACK) for x in tiles])
        return [x for x in tiles if self.game_object_proxy.get_attribute(x, AttributeType.ATTACK) == max_attack]
