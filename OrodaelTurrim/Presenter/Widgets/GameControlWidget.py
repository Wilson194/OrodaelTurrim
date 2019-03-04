from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Widgets.UnitWidget import UnitWidget
from OrodaelTurrim.Structure.Enums import GameObjectType
from OrodaelTurrim.Structure.Position import Position


class GameControlWidget(QWidget):
    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine

        self._scroll_area_layout = None
        self._scroll_area = None

        self.init_ui()


    def init_ui(self):
        with open(str(UI_ROOT / 'gameControlWidget.ui')) as f:
            uic.loadUi(f, self)

        self._scroll_area = self.findChild(QWidget, 'unitsArea')  # type: QWidget
        self._scroll_area_layout = QVBoxLayout(self)

        self._scroll_area.setLayout(self._scroll_area_layout)

        for game_object in GameObjectType.defenders():
            self._scroll_area_layout.addWidget(UnitWidget(self._scroll_area, self.__game_engine, game_object))

        Connector().subscribe('redraw_ui', self.redraw_available_money_slot)


    @pyqtSlot()
    def redraw_available_money_slot(self, position: Position = None):
        self.findChild(QLabel, 'moneyLabel').setText('Available money: {}'.format(
            self.__game_engine.get_resources(self.__game_engine.get_game_history().active_player)))
