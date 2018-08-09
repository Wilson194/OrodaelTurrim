import random
import sys
from typing import List

from ZNS.business.GameMap import GameMap
from ZNS.structure.Enums import TerrainType
from ZNS.structure.Position import AxialPosition, OffsetPosition, Position
from ZNS.structure.Terrain import River, Field, Terrain

RIVER_ON_MAP = 0.9
MOUNTAIN = 0.2
FIELD = 0.3
HILL = 0.2
FOREST = 0.2
VILLAGE = 0.01
PRECISION = 100


class MapGenerator:
    def __init__(self, width: int, height: int, seed: int = None):
        self.__width = width
        self.__height = height

        self.__vertical_radius = (height - 1) // 2
        self.__horizontal_radius = (width - 1) // 2

        self.__game_map = GameMap(width, height)

        if not seed:
            seed = random.randrange(sys.maxsize)

        random.seed(seed)

        print(seed)

        self.__base_random_list = self.create_base_random_list()

        for i in range(-self.__vertical_radius, self.__vertical_radius + 1):
            for j in range(-self.__horizontal_radius, self.__horizontal_radius + 1):
                self.__game_map.set_tile(OffsetPosition(i, j), Field())


    def create_base_random_list(self) -> List[TerrainType]:
        random_list = []

        for i in range(int(MOUNTAIN * PRECISION)):
            random_list.append(TerrainType.MOUNTAIN)

        for i in range(int(FIELD * PRECISION)):
            random_list.append(TerrainType.FIELD)

        for i in range(int(HILL * PRECISION)):
            random_list.append(TerrainType.HILL)

        for i in range(int(FOREST * PRECISION)):
            random_list.append(TerrainType.FOREST)

        for i in range(int(VILLAGE * PRECISION)):
            random_list.append(TerrainType.VILLAGE)

        return random_list


    def get_random_terrain_type(self, position: Position) -> Terrain:
        terrain_type = random.choice(self.__base_random_list)

        neigbours = position.get_all_neighbours()

        # for neigbour in neigbours

        return terrain_type.value


    def generate(self) -> GameMap:
        self.__generate_river()
        self.__generate_tiles()
        return self.__game_map


    def __generate_tiles(self):
        for i in range(-self.__vertical_radius, self.__vertical_radius + 1):
            for j in range(-self.__horizontal_radius, self.__horizontal_radius + 1):
                position = OffsetPosition(i, j)
                if self.__game_map[position].get_type() != TerrainType.RIVER:
                    self.__game_map.set_tile(position, self.get_random_terrain_type(position))


    def __generate_river(self):
        def filter_river_neighbour(position, ancestor):
            neighbours = [self.__game_map[x].get_type() for x in
                          self.__game_map.filter_positions_on_map(position.get_all_neighbours()) if ancestor != x]

            if TerrainType.RIVER in neighbours:
                return False

            return True


        if random.random() < RIVER_ON_MAP:
            SIDES = ['T', 'R', 'B', 'L']
            side = random.randint(0, 3)

            if SIDES[side] == 'T':
                position = random.randint(-self.__horizontal_radius, self.__horizontal_radius)
                start = OffsetPosition(position, -self.__vertical_radius)
                self.__game_map.set_tile(start, River())

            elif SIDES[side] == 'R':
                position = random.randint(-self.__vertical_radius, self.__vertical_radius)
                start = OffsetPosition(self.__horizontal_radius, position)
                self.__game_map.set_tile(start, River())

            elif SIDES[side] == 'B':
                position = random.randint(-self.__horizontal_radius, self.__horizontal_radius)
                start = OffsetPosition(position, self.__vertical_radius)
                self.__game_map.set_tile(start, River())

            elif SIDES[side] == 'L':
                position = random.randint(-self.__vertical_radius, self.__vertical_radius)
                start = OffsetPosition(-self.__horizontal_radius, position)
                self.__game_map.set_tile(start, River())

            current = start

            while True:
                # Filter neighbours on map
                neighbours = self.__game_map.filter_positions_on_map(current.get_all_neighbours())
                # Filter neighbours which are not RIVER
                neighbours = [x for x in neighbours if self.__game_map[x].get_type() != TerrainType.RIVER]
                # Filter neighbours which are have not river as neighbour
                neighbours = [x for x in neighbours if filter_river_neighbour(x, current)]

                neighbours.sort(key=lambda x: (x.length() + 1 if self.__game_map.position_on_edge(x) else 0))
                if neighbours:
                    for i in range(6):
                        neighbours.append(neighbours[0])

                neighbour = random.choice(neighbours)
                self.__game_map.set_tile(neighbour, River())
                if self.__game_map.position_on_edge(neighbour):
                    break
                else:
                    current = neighbour
