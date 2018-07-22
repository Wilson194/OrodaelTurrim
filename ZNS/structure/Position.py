from abc import ABC, abstractmethod


class Position(ABC):
    @abstractmethod
    def get_cubic_position(self) -> 'CubePosition':
        pass


class CubePosition(Position):
    def __init__(self, x_position: int, y_position: int, z_position: int) -> None:
        self.__x = x_position
        self.__y = y_position
        self.__z = z_position


    def get_cubic_position(self) -> 'CubePosition':
        return self


    @property
    def x(self) -> int:
        return self.__x


    @x.setter
    def x(self, value: int) -> None:
        self.__x = value


    @property
    def y(self) -> int:
        return self.__y


    @y.setter
    def y(self, value: int) -> None:
        self.__y = value


    @property
    def z(self) -> int:
        return self.__z


    @z.setter
    def z(self, value: int) -> None:
        self.__z = value
