from typing import Callable, Any

from OrodaelTurrim.Structure.Utils import Singleton


class Connector(metaclass=Singleton):
    def __init__(self):
        self._database = {}
        self._variables = {}


    def subscribe(self, name: str, target: Callable):
        if name in self._database:
            self._database[name].append(target)
        else:
            self._database[name] = [target]


    def emit(self, name: str, *args, **kwargs) -> None:
        for target in self._database.get(name, []):
            target(*args, **kwargs)


    def functor(self, name) -> "Caller":
        return Caller(name)


    def set_variable(self, name: str, value: Any) -> None:
        self._variables[name] = value


    def get_variable(self, name: str) -> Any:
        return self._variables.get(name, None)


class Caller:
    def __init__(self, name: str):
        self.__name = name


    def __call__(self, *args, **kwargs):
        Connector().emit(self.__name, *args, **kwargs)
