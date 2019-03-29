import time

from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject

from OrodaelTurrim.Business.GameEngine import GameEngine
# from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Connector import Connector


class WorkerSignals(QObject):
    redraw_signal = pyqtSignal()


class ThreadWorker(QRunnable):

    def __init__(self, game_engine: GameEngine, function_name: str, *args, **kwargs):
        super().__init__()
        self.game_engine = game_engine
        self.function_name = function_name
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()


    @pyqtSlot()
    def run(self):
        Connector().emit('game_thread_start')
        getattr(self.game_engine, self.function_name)(*self.args, **self.kwargs)
        Connector().emit('game_thread_finished')
