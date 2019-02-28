from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGraphicsSceneMouseEvent

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Widgets.LogWidget import LogWidget
from OrodaelTurrim.Presenter.Widgets.MapInfo import MapInfoWidget
from OrodaelTurrim.Presenter.Widgets.RoundControlWidget import RoundControlWidget


class ControlWidget(QWidget):
    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine

        self.map_info_widget = None

        self.init_ui()


    def init_ui(self):
        with open(str(UI_ROOT / 'controlWidget.ui')) as f:
            uic.loadUi(f, self)

        # Tab for map information
        map_tab = self.findChild(QWidget, 'mapTab')  # type: QWidget
        map_tab_layout = QVBoxLayout(map_tab)

        self.map_info_widget = MapInfoWidget(map_tab, self.__game_engine)
        map_tab_layout.addWidget(self.map_info_widget)

        # Tab for log information
        log_tab = self.findChild(QWidget, 'logTab')  # type: QWidget

        log_tab_layout = QVBoxLayout(log_tab)

        log_widget = LogWidget(log_tab, self.__game_engine)
        log_tab_layout.addWidget(log_widget)

        # Tab for game control
        round_tab = self.findChild(QWidget, 'roundTab')  # type: QWidget

        round_tab_layout = QVBoxLayout(round_tab)

        round_widget = RoundControlWidget(round_tab, self.__game_engine)
        round_tab_layout.addWidget(round_widget)


    @pyqtSlot()
    def run_inference_action(self, event: QGraphicsSceneMouseEvent):
        self.__game_engine.inference_turn()
