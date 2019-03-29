import copy
import multiprocessing
import random
from typing import List, TYPE_CHECKING, Dict, Union, Set
from OrodaelTurrim.Structure.Exceptions import IllegalArgumentException
from OrodaelTurrim.Structure.Position import Position, OffsetPosition
from collections import deque
from OrodaelTurrim.Structure.Enums import Nudge, HexDirection
from OrodaelTurrim.Structure.TypeStrucutre import DoubleLinkedList
from OrodaelTurrim.Structure.Utils import Singleton

if TYPE_CHECKING:
    from OrodaelTurrim.Structure.Enums import Nudge, TerrainType
    from OrodaelTurrim.Structure.Terrain import Terrain


class GameMap:
    def __init__(self, width: int, height: int, tiles: List[List['TerrainType']] = None):
        self.__size = (width, height)
        if width % 2 == 0 or height % 2 == 0:
            raise IllegalArgumentException('Map size must be odd numbers')

        self.__width = width
        self.__height = height

        self.__vertical_radius = (height - 1) // 2
        self.__horizontal_radius = (width - 1) // 2

        self.__visible_tiles_cache = {}

        self.__tiles = []  # type: List[List[Union[Terrain,None]]]
        for i in range(height):
            self.__tiles.append([])
            for j in range(width):
                self.__tiles[i].append(None)

        if tiles:
            for y, terrain_list in enumerate(tiles):
                for x, terrain_type in enumerate(terrain_list):
                    position = OffsetPosition(x - self.__horizontal_radius, y - self.__vertical_radius)
                    self.set_tile(position, terrain_type.value)


    def __sizeof__(self):
        return self.__size


    def __getitem__(self, position: Position) -> Union['Terrain', None]:
        position_offset = position.offset
        return self.__tiles[position_offset.q + self.__horizontal_radius][position_offset.r + self.__vertical_radius]


    def set_tile(self, position: Position, terrain: 'Terrain') -> None:
        """
        Set target position tile
        :param position: position which should be set
        :param terrain: terrain object for position
        """
        offset = self.__size[0] // 2, self.__size[1] // 2
        column = position.offset.q + offset[0]
        row = position.offset.r + offset[1]

        self.__tiles[column][row] = terrain


    @property
    def tiles(self):
        """
        Iterator for all map tiles
        """
        for y in range(-self.__horizontal_radius, self.__horizontal_radius + 1):
            for x in range(-self.__vertical_radius, self.__vertical_radius + 1):
                yield OffsetPosition(y, x)


    @property
    def size(self):
        return self.__width, self.__height


    @property
    def width(self) -> int:
        return self.__width


    @property
    def height(self) -> int:
        return self.__height


    @property
    def vertical_radius(self) -> int:
        return self.__vertical_radius


    @property
    def horizontal_radius(self) -> int:
        return self.__horizontal_radius


    def position_on_map(self, position: Position) -> bool:
        """
        Check if position is on map
        :param position: target position
        :return: True if position is on map, False otherwise
        """
        x = position.offset.r
        y = position.offset.q

        return - self.__vertical_radius <= x <= self.__vertical_radius and - self.__horizontal_radius <= y <= self.__horizontal_radius


    def filter_positions_on_map(self, positions: List[Position]):
        on_map_positions = []
        for position in positions:
            if self.position_on_map(position):
                on_map_positions.append(position)

        return on_map_positions


    def position_on_edge(self, position: Position) -> bool:
        x = position.offset.r
        y = position.offset.q

        return self.__vertical_radius == x or -self.__vertical_radius == x or self.__horizontal_radius == y or -self.__horizontal_radius == y


    def can_been_seen(self, start: Position, end: Position, sight: int, nudge: 'Nudge') -> bool:
        if start == end:
            return True
        line = start.plot_line(end, nudge)

        for tile in line[1:-1]:
            int_tile = tile.int_coord.offset
            if not self.position_on_map(int_tile):
                return False
            sight = self[int_tile].get_remaining_sigh(sight)

        return sight > 0


    def get_visible_tiles(self, position: Position, sight: int) -> Set[Position]:
        if not self.position_on_map(position):
            return set()

        if position in self.__visible_tiles_cache and sight in self.__visible_tiles_cache[position]:
            return copy.deepcopy(self.__visible_tiles_cache[position][sight])

        visited = set()
        visible = set()
        pool = set()
        pool.add(position)

        while len(pool) > 0:
            current = pool.pop()

            if current not in visited:
                visited.add(current)
            else:
                continue

            if current not in visible and (
                    self.can_been_seen(position, current, sight, Nudge.NEGATIVE) or self.can_been_seen(position,
                                                                                                       current, sight,
                                                                                                       Nudge.POSITIVE)):
                visible.add(current)

            for tile in current.get_all_neighbours():
                if self.position_on_map(tile) and tile not in visited:
                    pool.add(tile)

        if position not in self.__visible_tiles_cache:
            self.__visible_tiles_cache[position] = {}
        if sight not in self.__visible_tiles_cache[position]:
            self.__visible_tiles_cache[position][sight] = copy.deepcopy(visible)

        return visible


    def get_accessible_tiles(self, position: Position, actions: int) -> Dict[Position, int]:
        if not self.position_on_map(position):
            return {}

        pool = deque()
        pool.append(position)

        result_map = {position: actions}

        while len(pool) != 0:
            current = pool.popleft()
            current_actions = result_map[current]

            for neighbour in current.get_all_neighbours():
                if self.position_on_map(neighbour):
                    move_cost = self[current].get_move_cost(self[neighbour].terrain_type)
                    remaining = current_actions - move_cost

                    if remaining >= 0 and (neighbour not in result_map or result_map[neighbour] < remaining):
                        result_map[neighbour] = remaining
                        pool.append(neighbour)

        return result_map


    @property
    def border_tiles(self) -> Set[Position]:
        border_tiles = set()
        for x in range(-self.__horizontal_radius, self.__horizontal_radius + 1):
            border_tiles.add(OffsetPosition(x, -self.__vertical_radius))
            border_tiles.add(OffsetPosition(x, self.__vertical_radius))

        for y in range(-self.__vertical_radius, self.__vertical_radius + 1):
            border_tiles.add(OffsetPosition(-self.__horizontal_radius, y))
            border_tiles.add(OffsetPosition(self.__horizontal_radius, y))

        return border_tiles


    def __repr__(self):
        map_repr = ''
        for i, row in enumerate(self.__tiles):
            if i % 2 == 1:
                map_repr += ' '
            for column in row:
                map_repr += column.char()
                map_repr += ' '

            map_repr += '\n'

        return map_repr


class BorderTiles(metaclass=Singleton):
    def __init__(self, game_map: GameMap = None):
        self.__game_map = game_map

        self.__border_tiles = DoubleLinkedList()
        self.__create_linked_list()


    def get_position(self, starting_position: Position, shift: int) -> Position:
        self.__border_tiles.pointer = self.__border_tiles.head

        while self.__border_tiles.value != starting_position:
            self.__border_tiles.next()

        for i in range(abs(shift)):
            if shift < 0:
                self.__border_tiles.previous()
            else:
                self.__border_tiles.next()

        return self.__border_tiles.value


    def get_position_list(self, starting_position: Position, length: int) -> List[Position]:
        self.__border_tiles.pointer = self.__border_tiles.head

        while self.__border_tiles.value != starting_position:
            self.__border_tiles.next()

        result_list = []
        for i in range(length):
            result_list.append(self.__border_tiles.value)
            self.__border_tiles.next()

        return result_list


    def __create_linked_list(self):
        PRECEDENCE = {OffsetPosition(self.__game_map.horizontal_radius, self.__game_map.vertical_radius),
                      OffsetPosition(-self.__game_map.horizontal_radius, self.__game_map.vertical_radius)}

        first = OffsetPosition(-self.__game_map.horizontal_radius, -self.__game_map.vertical_radius)
        second = OffsetPosition(-self.__game_map.horizontal_radius + 1, -self.__game_map.vertical_radius)
        self.__border_tiles.push_back(first)
        self.__border_tiles.push_back(second)

        tiles = self.__game_map.border_tiles
        tiles.remove(first)
        tiles.remove(second)

        current = self.__border_tiles.head.value
        while tiles:
            _next_set = set(current.get_all_neighbours()).intersection(tiles)
            if len(_next_set) > 1:
                _next_set = _next_set.intersection(PRECEDENCE)

            _next = _next_set.pop()

            current = _next
            self.__border_tiles.push_back(_next)
            tiles.remove(_next)

        self.__border_tiles.head.next = self.__border_tiles.tail
        self.__border_tiles.tail.previous = self.__border_tiles.head
