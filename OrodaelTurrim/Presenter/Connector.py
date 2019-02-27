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


    def functor(self, name):
        if name in self.__database:
            return self.__database[name]
        else:
            return Caller(name)


class Caller:
    def __init__(self, name: str):
        self.__connector = Connector()
        self.__name = name


    def __call__(self, *args, **kwargs):
        return self.__connector.connector(self.__name, *args, **kwargs)
