from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QPushButton

from ZNS.business.GameEngine import GameEngine

PATH_RES = Path(__file__).parent.parent / 'res'


class ControlWidget(QWidget):
    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)
        self.__game_engine = game_engine

        with open(str(PATH_RES / 'ui' / 'controlWidget.ui')) as f:
            uic.loadUi(f, self)

        self.init_ui()

    def init_ui(self):
        run_inference_button = self.findChild(QPushButton, 'runInferenceButton')
        run_inference_button.clicked.connect(self.run_inference_action)

    @pyqtSlot()
    def run_inference_action(self):
        self.__game_engine.inference_turn()
