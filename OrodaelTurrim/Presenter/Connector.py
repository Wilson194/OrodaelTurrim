import sys
from typing import Callable, Any

from PyQt5.QtCore import pyqtSignal, QObject
from OrodaelTurrim.Structure.Utils import QtSingleton

from OrodaelTurrim.Structure.Position import Position
import threading


class Connector(QObject, metaclass=QtSingleton):
    _lock = threading.Lock()
    redraw_ui = pyqtSignal()
    redraw_map = pyqtSignal()
    display_border = pyqtSignal(dict, list)
    game_over = pyqtSignal()
    map_position_change = pyqtSignal(Position)
    history_action = pyqtSignal()
    status_message = pyqtSignal(str)
    update_log = pyqtSignal()
    log_message = pyqtSignal(str)

    game_thread_finished = pyqtSignal()


    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._variables = {}


    def subscribe(self, name: str, target: Callable):
        try:
            getattr(self, name).connect(target)
        except AttributeError:
            sys.stderr.write('Signal {} not defined, signal not subscribed!\n'.format(name))


    def emit(self, name: str, *args, **kwargs) -> None:
        try:
            getattr(self, name).emit(*args, **kwargs)
        except AttributeError:
            sys.stderr.write('Signal {} not defined, signal not emitted!\n'.format(name))


    def functor(self, name) -> "Caller":
        return Caller(name)


    def set_variable(self, name: str, value: Any) -> None:
        with self._lock:
            self._variables[name] = value


    def get_variable(self, name: str) -> Any:
        with self._lock:
            return self._variables.get(name, None)


class Caller:
    def __init__(self, name: str):
        self.__name = name


    def __call__(self, *args, **kwargs):
        Connector().emit(self.__name, *args, **kwargs)
