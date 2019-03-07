from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QTextEdit

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector


class LogWidget(QWidget):

    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine

        self.init_ui()

        self.__text_area = self.findChild(QTextEdit, 'logText')  # type: QTextEdit

        self.update_text()


    def init_ui(self):
        with open(str(UI_ROOT / 'logWidget.ui')) as f:
            uic.loadUi(f, self)

        Connector().subscribe('redraw_ui', self.update_text)


    @pyqtSlot()
    def update_text(self):
        history = self.__game_engine.get_game_history()

        self.__text_area.setText(str(history))
