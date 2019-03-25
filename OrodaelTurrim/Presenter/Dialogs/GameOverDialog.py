from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QPushButton

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Structure.Enums import GameOverStates


class GameOverDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

        self.findChild(QPushButton, 'findReasonButton').clicked.connect(self.find_reason_slot)
        self.findChild(QPushButton, 'letHimDieButton').clicked.connect(self.let_him_die_slot)


    def init_ui(self):
        with open(str(UI_ROOT / 'gameOverDialog.ui')) as f:
            uic.loadUi(f, self)


    @pyqtSlot()
    def find_reason_slot(self):
        self.done(GameOverStates.FIND_REASON.value)


    @pyqtSlot()
    def let_him_die_slot(self):
        self.done(GameOverStates.LET_HIM_DIE.value)


    @staticmethod
    def execute_():
        dialog = GameOverDialog()
        result = dialog.exec_()

        return result
