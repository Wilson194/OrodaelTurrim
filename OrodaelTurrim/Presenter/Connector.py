from typing import Callable

from OrodaelTurrim.Structure.Utils import Singleton


class Connector(metaclass=Singleton):
    def __init__(self):
        self.__database = {}

    def subscribe(self, name: str, target: Callable):
        self.__database[name] = target

    def connector(self, name, *args, **kwargs):
        if name in self.__database:
            self.__database[name](*args, **kwargs)
