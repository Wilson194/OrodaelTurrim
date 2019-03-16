from typing import List, Dict, Tuple

from OrodaelTurrim.Business.Interface.Player import IAttacker
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy, GameUncertaintyProxy
from OrodaelTurrim.Structure.Enums import GameRole, GameObjectType
from OrodaelTurrim.Structure.Exceptions import IllegalActionException
from OrodaelTurrim.Structure.Filter.AttackFilter import AttackBaseFilter, AttackMostVulnerableFilter, \
    AttackNearestFilter, AttackNoResistantFilter, AttackStrongestFilter
from OrodaelTurrim.Structure.Filter.FilterPattern import AttackFilter, MoveFilter
from OrodaelTurrim.Structure.Filter.MoveFilter import MoveToNearestEnemyFilter, MoveToRangeFilter, MoveToBaseFilter, \
    MoveToSafeDistanceFilter
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation


class AIPlayer(IAttacker):
    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy, game_control_proxy: GameControlProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy):
        super().__init__(map_proxy, game_object_proxy, game_control_proxy, game_uncertainty_proxy)

        self.__spawn_information = None  # type : List[List[SpawnInformation]
        self.__resources_left = None
        self.most_expensive_unit = None
        self.border_tiles = None


    def act(self) -> None:
        print('Rigor Mortis doing his stuff')
        if self.__spawn_information is None:
            self.__initialize()

        for spawn in self.spawn_information_list[0]:
            try:
                self.game_control_proxy.spawn_unit(spawn)
            except IllegalActionException:
                pass

        self.__update_spawn_list()


    @property
    def spawn_information_list(self) -> List[List[SpawnInformation]]:
        return self.__spawn_information


    @property
    def name(self) -> str:
        return 'Rigor Mortis'


    def __initialize(self):
        self.__spawn_information = [[] for _ in range(3)]  # type : List[List[SpawnInformation]

        # List of GameObject for attackers
        self.attackers = GameObjectType.attackers()

        # Most expensive unit
        max_price = max([x.price for x in self.attackers])
        self.most_expensive_unit = [x for x in self.attackers if x.price == max_price][0]

        # Cheapest unit
        min_price = min([x.price for x in self.attackers])
        self.cheapest_unit = [x for x in self.attackers if x.price == min_price][0]

        # Border tiles
        self.border_tiles = self.map_proxy.border_tiles

        self.__prepare_units_filters()

        self.__initialize_spawn_list()


    def __prepare_units_filters(self):
        nearest_enemy = MoveToNearestEnemyFilter(self.map_proxy, self.game_object_proxy)
        to_range = MoveToRangeFilter(self.map_proxy, self.game_object_proxy)
        to_base = MoveToBaseFilter(self.map_proxy, self.game_object_proxy)
        safe_dist = MoveToSafeDistanceFilter(self.map_proxy, self.game_object_proxy)

        base = AttackBaseFilter(self.map_proxy, self.game_object_proxy)
        vulnerable = AttackMostVulnerableFilter(self.map_proxy, self.game_object_proxy)
        nearest = AttackNearestFilter(self.map_proxy, self.game_object_proxy)
        no_resistance = AttackNoResistantFilter(self.map_proxy, self.game_object_proxy)
        strongest = AttackStrongestFilter(self.map_proxy, self.game_object_proxy)

        self.unit_filters = {
            GameObjectType.CYCLOPS: ([vulnerable], [nearest_enemy, to_base]),
            GameObjectType.DEMON: ([no_resistance, strongest], [to_range]),
            GameObjectType.ELEMENTAL: ([strongest, vulnerable], [safe_dist]),
            GameObjectType.GARGOYLE: ([base], [to_base]),
            GameObjectType.MINOTAUR: ([vulnerable], [nearest_enemy, to_base]),
            GameObjectType.NECROMANCER: ([], [safe_dist]),
            GameObjectType.ORC: ([nearest, base], [nearest_enemy, to_base]),
            GameObjectType.SKELETON: ([nearest, base], [nearest_enemy, to_base]),
        }  # type: Dict[GameObjectType,Tuple[List[AttackFilter], List[MoveFilter]]]


    def __initialize_spawn_list(self):
        resources = self.map_proxy.get_resources(self)
        income = self.map_proxy.get_income(self)

        for round_list in self.spawn_information_list:
            # Generate list of spawn info for one round
            round_spawn, spend = self.__create_round_list(resources)

            # Set list to the spawn info
            round_list.extend(round_spawn)

            # Update resources_left
            resources = resources - spend + income

        self.__resources_left = resources


    def __update_spawn_list(self):
        self.spawn_information_list.pop(0)

        _round, spend = self.__create_round_list(self.__resources_left)

        self.spawn_information_list.append(_round)
        self.__resources_left = self.__resources_left + self.map_proxy.get_income(self) - spend


    def __create_round_list(self, resources: int) -> Tuple[List[SpawnInformation], int]:
        result = []
        spend = 0
        current_resources = resources
        while self.__spawn_unit(resources, current_resources):
            spawn_info = self.__create_spawn_info(current_resources)
            current_resources -= spawn_info.object_type.price
            spend += spawn_info.object_type.price
            result.append(spawn_info)

        return result, spend


    def __create_spawn_info(self, resources: int) -> SpawnInformation:

        attackers = [attacker for attacker in self.attackers if attacker.price <= resources]
        game_object = self.spawn_random.choice(attackers)

        free_border_tiles = [tile for tile in self.border_tiles if
                             self.game_object_proxy.get_object_type(tile) == GameObjectType.NONE]

        position = self.spawn_random.choice(tuple(free_border_tiles))
        return SpawnInformation(self, game_object, position, self.unit_filters[game_object][0],
                                self.unit_filters[game_object][1])


    def __spawn_unit(self, maximum_resources: int, remaining_resources: int) -> bool:
        """ Determinate if spawn new unit or not"""
        if remaining_resources > self.most_expensive_unit.price:
            return True

        if remaining_resources < self.cheapest_unit.price:
            return False

        bound = maximum_resources / remaining_resources
        if bound > self.spawn_random.random():
            return True
        else:
            return False
