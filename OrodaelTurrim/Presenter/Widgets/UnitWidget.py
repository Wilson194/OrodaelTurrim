from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Utils import AssetsEncoder
from OrodaelTurrim.Structure.Enums import GameObjectType


class UnitWidget(QWidget):
    def __init__(self, parent=None, game_engine: GameEngine = None, object_type: GameObjectType = None):
        super().__init__(parent)

        self.__game_engine = game_engine
        self.__object_type = object_type

        self.init_ui()


    def init_ui(self):
        with open(str(UI_ROOT / 'unitFrameWidget.ui')) as f:
            uic.loadUi(f, self)

        img = AssetsEncoder[self.__object_type]

        img_label = self.findChild(QLabel, 'imageLabel')  # type: QLabel
        name_label = self.findChild(QLabel, 'nameLabel')  # type: QLabel

        img_label.setPixmap(QPixmap(str(img)).scaled(100, 100, Qt.KeepAspectRatio))
        # img_label.setScaledContents(True)

        name_label.setText(self.__object_type.name.capitalize())
