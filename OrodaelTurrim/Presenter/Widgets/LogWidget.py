from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine


class LogWidget(QWidget):

    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine
        self.__selected_tile = None
        self.label = None

        self.init_ui()


    def init_ui(self):
        with open(str(UI_ROOT / 'logWidget.ui')) as f:
            uic.loadUi(f, self)
