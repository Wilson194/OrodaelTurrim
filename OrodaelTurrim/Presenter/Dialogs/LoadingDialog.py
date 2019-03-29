from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog

from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Dialogs.GameOverDialog import GameOverDialog


class LoadingDialog(QDialog):

    def __init__(self):
        super().__init__()

        # print('---->', signals.finished)
        # signals.finished.connect(self.accept)
        # Connector().subscribe('game_over', self.accept)


    @staticmethod
    def execute_():
        dialog = LoadingDialog()
        result = dialog.exec_()

        return result
