from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QPushButton

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.business.GameEngine import GameEngine


class ControlWidget(QWidget):
    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)
        self.__game_engine = game_engine

        with open(str(UI_ROOT / 'controlWidget.ui')) as f:
            uic.loadUi(f, self)

        self.init_ui()

    def init_ui(self):
        run_inference_button = self.findChild(QPushButton, 'runInferenceButton')
        run_inference_button.clicked.connect(self.run_inference_action)

    @pyqtSlot()
    def run_inference_action(self):
        self.__game_engine.inference_turn()
