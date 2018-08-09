import random
from typing import List, TYPE_CHECKING, Dict
from ZNS.structure.Exceptions import IllegalArgumentException
from ZNS.structure.Position import Position, OffsetPosition
from collections import deque


if TYPE_CHECKING:
    from ZNS.structure.Enums import Nudge, TerrainType
    from ZNS.structure.Terrain import Terrain


class GameMap:
    def __init__(self, width: int, height: int, tiles: List[List['TerrainType']] = None):
        self.__size = (width, height)
        if width % 2 == 0 or height % 2 == 0:
            raise IllegalArgumentException('Map size must be odd numbers')

        self.__vertical_radius = (height - 1) // 2
        self.__horizontal_radius = (width - 1) // 2

        self.__tiles = []
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


    def __getitem__(self, position: Position) -> 'Terrain':
        return self.__tiles[position.offset.q + self.__horizontal_radius][position.offset.r + self.__vertical_radius]


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

        print(x, y, self.__vertical_radius, self.__horizontal_radius)


        return self.__vertical_radius == x or -self.__vertical_radius == x or self.__horizontal_radius == y or -self.__horizontal_radius == y


    def can_been_seen(self, start: Position, end: Position, sight: int, nudge: 'Nudge') -> bool:
        if start == end:
            return True
        line = start.plot_line(end, nudge)

        for tile in line[1:-1]:
            sight = self[tile.int_coord].get_remaining_sigh(sight)

        return sight > 0


    def get_visible_tiles(self, position: Position, sight: int) -> List[Position]:
        from ZNS.structure.Enums import Nudge
        if not self.position_on_map(position):
            return []
        visited = []
        visible = []
        pool = deque()
        pool.append(position)

        while len(pool) > 0:
            current = pool.popleft()

            if current not in visited:
                visited.append(current)

            if current not in visible and (
                    self.can_been_seen(position, current, sight, Nudge.NEGATIVE) or self.can_been_seen(position, current, sight,
                                                                                                       Nudge.POSITIVE)):
                visible.append(current)

            for tile in current.get_all_neighbours():
                if self.position_on_map(tile) and tile not in visited:
                    pool.append(tile)

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
                    move_cost = self[current].get_move_cost(self[neighbour].get_type())
                    remaining = current_actions - move_cost

                    if remaining >= 0 and (neighbour not in result_map or result_map[neighbour] < remaining):
                        result_map[neighbour] = remaining
                        pool.append(neighbour)

        return result_map


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
