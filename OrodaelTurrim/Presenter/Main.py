from pathlib import Path

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QSplitter, QWidget, QMessageBox, QSystemTrayIcon

from OrodaelTurrim import ICONS_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Widgets.ControlWidget import ControlWidget
from OrodaelTurrim.Presenter.Widgets.MapWidget import MapWidget
from OrodaelTurrim.Structure.Position import Position

PATH_RES = Path(__file__).parent.parent / 'res'


class MainWidget(QWidget):
    """ Main widget with QSplit - Map / Control"""


    def __init__(self, parent: QWidget = None, game_engine: GameEngine = None):
        super().__init__(parent)
        self.__game_engine = game_engine

        self.init_ui()


    def init_ui(self):
        hbox = QHBoxLayout(self)

        # Left frame for map
        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)

        # Right frame for control tabs
        right = QFrame(self)
        right.setFrameShape(QFrame.StyledPanel)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(left)
        splitter1.addWidget(right)
        splitter1.setSizes([100, 70])

        hbox.addWidget(splitter1)
        self.setLayout(hbox)

        # Create map widget in left split
        map_layout = QHBoxLayout(left)

        map_widget = MapWidget(self, self.__game_engine)
        map_layout.addWidget(map_widget)
        left.setLayout(map_layout)

        # Create control widget in right split
        control_layout = QHBoxLayout(right)
        control_widget = ControlWidget(right, self.__game_engine)
        control_layout.addWidget(control_widget)
        right.setLayout(control_layout)


class MainWindow(QObject):
    """ Main windows class with QApplication instance """


    def __init__(self, game_engine: GameEngine):
        super().__init__()
        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QMainWindow()

        with open(str(PATH_RES / 'ui' / 'main.ui')) as f:
            uic.loadUi(f, self.window)

        central = self.window.findChild(QtWidgets.QWidget, 'centralWidget')

        layout = QHBoxLayout()
        main_widget = MainWidget(self.window, game_engine)
        layout.addWidget(main_widget)
        central.setLayout(layout)

        Connector().subscribe('status_message', self.status_info)
        Connector().subscribe('map_position_change', self.tile_selected)
        Connector().subscribe('map_position_clear', self.tile_unselected)
        Connector().subscribe('error_message', self.error_message_slot)


    def execute(self) -> int:
        """ Display main window and start loop """
        self.window.show()
        self.window.showMaximized()

        # Window icon
        self.window.setWindowIcon(QIcon(str(ICONS_ROOT / 'game_icon.png')))
        self.window.setWindowTitle('Orodael Turrim')

        QSystemTrayIcon(QIcon(str(ICONS_ROOT / 'game_icon.png')), self.app)

        self.app.setWindowIcon(QIcon(str(ICONS_ROOT / 'game_icon.png')))

        return self.app.exec()


    def tile_selected(self, position: Position) -> None:
        """ Display selected position in windows status bar """
        if position:
            text = '     Offset: {}, Cubic: {}, Axial: {}'.format(position.offset.string, position.cubic.string,
                                                                  position.axial.string)
            self.status_info(text)
        else:
            self.status_info('No tile selected')


    def tile_unselected(self) -> None:
        """ Clear status bar"""
        self.status_info('No tile selected')


    def status_info(self, text: str) -> None:
        """ Display text on status bar"""
        self.window.statusBar().showMessage(text)


    @pyqtSlot(str, str)
    def error_message_slot(self, context: str, error_message: str) -> None:
        """ Display error window with error message """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error_message)
        msg.setWindowTitle('Error: ' + context)
        msg.exec_()
