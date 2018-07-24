from ZNS.structure.Exceptions import IllegalArgumentException
from ZNS.structure.Position import Position, OffsetPosition
from ZNS.structure.Terrain import Terrain, Mountain


class Map:
    def __init__(self, width: int, height: int):
        self.__size = (width, height)
        if width % 2 == 0 or height % 2 == 0:
            raise IllegalArgumentException('Map size must be odd numbers')

        self.__tiles = [[Mountain() for x in range(height)] for y in range(width)]

        self.__vertical_radius = (height - 1) // 2
        self.__horizontal_radius = (width - 1) // 2


    def __sizeof__(self):
        return self.__size


    def __getitem__(self, position: Position) -> Terrain:
        print(position)
        print(self.__horizontal_radius)
        print(self.__vertical_radius)
        return self.__tiles[position.offset.q + self.__horizontal_radius][position.offset.r + self.__vertical_radius]


    def set_tile(self, position: Position, terrain: Terrain):
        offset = self.__size[0] // 2, self.__size[1] // 2
        column = position.offset.q + offset[0]
        row = position.offset.r + offset[1]

        self.__tiles[column][row] = terrain


    @property
    def tiles(self):
        for y in range(-self.__horizontal_radius, self.__horizontal_radius + 1):
            for x in range(-self.__vertical_radius, self.__vertical_radius + 1):
                yield OffsetPosition(y, x)
