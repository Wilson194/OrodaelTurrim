from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Widgets.UnitWidget import UnitWidget
from OrodaelTurrim.Structure.Enums import GameObjectType


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

        self._scroll_area = self.findChild(QScrollArea, 'unitsArea')  # type: QScrollArea
        self._scroll_area_layout = QVBoxLayout(self._scroll_area)

        self._scroll_area_layout.addWidget(UnitWidget(self._scroll_area, self.__game_engine, GameObjectType.BASE))
        self._scroll_area_layout.addWidget(UnitWidget(self._scroll_area, self.__game_engine, GameObjectType.BASE))
        self._scroll_area_layout.addWidget(UnitWidget(self._scroll_area, self.__game_engine, GameObjectType.BASE))
        self._scroll_area_layout.addWidget(UnitWidget(self._scroll_area, self.__game_engine, GameObjectType.BASE))
        self._scroll_area_layout.addWidget(UnitWidget(self._scroll_area, self.__game_engine, GameObjectType.BASE))
        self._scroll_area_layout.addWidget(UnitWidget(self._scroll_area, self.__game_engine, GameObjectType.BASE))

        self._scroll_area.setLayout(self._scroll_area_layout)
