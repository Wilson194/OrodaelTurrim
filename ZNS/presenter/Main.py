from pathlib import Path

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QFrame, QSplitter, QWidget

from ZNS.business.GameEngine import GameEngine
from ZNS.presenter.Control import ControlWidget
from ZNS.presenter.Map import MapWidget

PATH_RES = Path(__file__).parent.parent / 'res'


class MainWidget(QWidget):
    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)
        self.__game_engine = game_engine

        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout(self)

        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)

        right = QFrame(self)
        right.setFrameShape(QFrame.StyledPanel)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(left)
        splitter1.addWidget(right)
        splitter1.setSizes([100, 100])

        hbox.addWidget(splitter1)
        self.setLayout(hbox)

        map_layout = QHBoxLayout(left)

        map_widget = MapWidget(left, self.__game_engine)
        map_layout.addWidget(map_widget)
        left.setLayout(map_layout)

        control_layout = QHBoxLayout(right)
        control_widget = ControlWidget(right, self.__game_engine)
        control_layout.addWidget(control_widget)
        right.setLayout(control_layout)


class MainWindow:
    def __init__(self, game_engine: GameEngine):
        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QMainWindow()

        with open(str(PATH_RES / 'ui' / 'main.ui')) as f:
            uic.loadUi(f, self.window)

        central = self.window.findChild(QtWidgets.QWidget, 'centralWidget')

        layout = QHBoxLayout()
        main_widget = MainWidget(self.window, game_engine)
        layout.addWidget(main_widget)
        central.setLayout(layout)

    def execute(self):
        self.window.show()
        self.window.showMaximized()

        return self.app.exec()
