import typing

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QTextEdit

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector


class LogWidget(QWidget):
    """ Widget for displaying log information"""


    def __init__(self, parent: QWidget = None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine

        Connector().subscribe('redraw_ui', self.update_text)
        Connector().subscribe('game_thread_finished', self.update_text)

        self.init_ui()
        self.__text_area = typing.cast(QTextEdit, self.findChild(QTextEdit, 'logText'))


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'logWidget.ui')) as f:
            uic.loadUi(f, self)


    @pyqtSlot()
    def update_text(self) -> None:
        """ Set text of the text edit to output from GameHistory"""
        history = self.__game_engine.get_game_history()

        self.__text_area.setText(str(history))
