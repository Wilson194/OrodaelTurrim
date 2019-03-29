from PyQt5 import uic, QtCore
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog, QLabel

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Dialogs.GameOverDialog import GameOverDialog


class LoadingDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.init_ui()

        Connector().subscribe('game_over', self.accept)
        Connector().subscribe('game_thread_finished', self.accept)


    def init_ui(self):
        with open(str(UI_ROOT / 'loadingDialog.ui')) as f:
            uic.loadUi(f, self)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)


    @staticmethod
    def execute_():
        dialog = LoadingDialog()
        result = dialog.exec_()

        return result
