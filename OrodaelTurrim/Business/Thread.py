import time

from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject

from OrodaelTurrim.Business.GameEngine import GameEngine
# from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Dialogs.LoadingDialog import LoadingDialog
from threading import Lock

class WorkerSignals(QObject):
    redraw_signal = pyqtSignal()


class ThreadWorker(QRunnable):
    _lock = Lock()
    def __init__(self, game_engine: GameEngine, function_name: str, *args, **kwargs):
        super().__init__()
        self.game_engine = game_engine
        self.function_name = function_name
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()


    @pyqtSlot()
    def run(self):
        self._lock.acquire()
        time.sleep(0.1)
        getattr(self.game_engine, self.function_name)(*self.args, **self.kwargs)
        Connector().emit('game_thread_finished')
        self._lock.release()
        # LoadingDialog.execute_()