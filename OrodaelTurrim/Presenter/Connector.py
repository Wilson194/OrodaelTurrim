from typing import Callable

from OrodaelTurrim.Structure.Utils import Singleton


class Connector(metaclass=Singleton):
    def __init__(self):
        self._database = {}


    def subscribe(self, name: str, target: Callable):
        if name in self._database:
            self._database[name].append(target)
        else:
            self._database[name] = [target]


    def emit(self, name, *args, **kwargs):
        for target in self._database.get(name, []):
            target(*args, **kwargs)


    def functor(self, name):
        return Caller(name)


class Caller:
    def __init__(self, name: str):
        self.__name = name


    def __call__(self, *args, **kwargs):
        Connector().emit(self.__name, *args, **kwargs)
