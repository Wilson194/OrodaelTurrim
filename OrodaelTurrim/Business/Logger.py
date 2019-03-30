import sys
from typing import TYPE_CHECKING

from PyQt5.QtCore import pyqtSlot, QObject

from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Structure.Exceptions import IllegalLogMessage

if TYPE_CHECKING:
    from OrodaelTurrim.Business.GameEngine import GameEngine


class Logger:
    @staticmethod
    def log(text: str):
        if type(text) != str:
            raise IllegalLogMessage('Log messages must be string type')

        Connector().emit('log_message', text)


class LogReceiver(QObject):
    def __init__(self, game_engine: "GameEngine"):
        super().__init__()
        self.game_engine = game_engine

        Connector().subscribe('log_message', self.create_log_record_slot)


    @pyqtSlot(str)
    def create_log_record_slot(self, message: str):
        self.game_engine.create_log_action(message)
