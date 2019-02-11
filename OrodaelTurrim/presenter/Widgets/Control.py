from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGraphicsSceneMouseEvent

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.business.GameEngine import GameEngine
from OrodaelTurrim.presenter.Widgets.MapInfo import MapInfoWidget


class ControlWidget(QWidget):
    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine

        self.map_info_widget = None

        self.init_ui()

    def init_ui(self):
        with open(str(UI_ROOT / 'controlWidget.ui')) as f:
            uic.loadUi(f, self)

        map_tab = self.findChild(QWidget, 'mapTab')  # type: QWidget
        map_tab_layout = QVBoxLayout(map_tab)

        self.map_info_widget = MapInfoWidget(map_tab, self.__game_engine)

        map_tab_layout.addWidget(self.map_info_widget)

        # run_inference_button = self.findChild(QPushButton, 'runInferenceButton')
        # run_inference_button.clicked.connect(self.run_inference_action)

    @pyqtSlot()
    def run_inference_action(self, event: QGraphicsSceneMouseEvent):
        self.__game_engine.inference_turn()
