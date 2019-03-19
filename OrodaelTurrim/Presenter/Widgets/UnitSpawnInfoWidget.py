from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Presenter.Utils import AssetsEncoder
from OrodaelTurrim.Structure.GameObjects.GameObject import UncertaintySpawn


class UnitSpawnInfoWidget(QWidget):
    def __init__(self, parent=None, uncertainty_spawn: UncertaintySpawn = None):
        super().__init__(parent)

        self.uncertainty_spawn = uncertainty_spawn
        self.init_ui()


    def init_ui(self):
        with open(str(UI_ROOT / 'unitSpawnInfoWidget.ui')) as f:
            uic.loadUi(f, self)

        img = AssetsEncoder[self.uncertainty_spawn.game_object_type]

        img_label = self.findChild(QLabel, 'imageLabel')  # type: QLabel
        unit_label = self.findChild(QLabel, 'unitLabel')  # type: QLabel
        position_label = self.findChild(QLabel, 'positionLabel')  # type: QLabel

        img_label.setScaledContents(True)
        img_label.setPixmap(QPixmap(str(img)))

        unit_label.setText('Unit: {} ({}%)'.format(self.uncertainty_spawn.game_object_type.name.capitalize(),
                                                   self.uncertainty_spawn.object_uncertainty*100))
        position_label.setText('Position: {} ({}%)'.format(self.uncertainty_spawn.position,
                                                           self.uncertainty_spawn.position_uncertainty*100))
