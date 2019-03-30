from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Widgets.UnitSpawnInfoWidget import UnitSpawnInfoWidget
from OrodaelTurrim.Structure.Enums import GameObjectType


class SpawnInfoWidget(QWidget):
    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine

        self.__round_1_layout = None  # type: QVBoxLayout
        self.__round_2_layout = None  # type: QVBoxLayout
        self.__round_3_layout = None  # type: QVBoxLayout

        self.__round_1_box = None
        self.__round_2_box = None
        self.__round_3_box = None

        Connector().subscribe('redraw_ui', self.redraw_ui)
        Connector().subscribe('game_thread_finished', self.redraw_ui)

        self.init_ui()


    def init_ui(self):
        with open(str(UI_ROOT / 'spawnInfoWidget.ui')) as f:
            uic.loadUi(f, self)

        self.__round_1_box = self.findChild(QWidget, 'round1BoxWidget')  # type:QWidget
        self.__round_2_box = self.findChild(QWidget, 'round2BoxWidget')  # type:QWidget
        self.__round_3_box = self.findChild(QWidget, 'round3BoxWidget')  # type:QWidget

        self.__round_1_layout = QVBoxLayout(self.__round_1_box)
        self.__round_1_box.setLayout(self.__round_1_layout)

        self.__round_2_layout = QVBoxLayout(self.__round_2_box)
        self.__round_2_box.setLayout(self.__round_2_layout)

        self.__round_3_layout = QVBoxLayout(self.__round_3_box)
        self.__round_3_box.setLayout(self.__round_3_layout)


    def redraw_ui(self):
        current_turn = self.__game_engine.get_game_history().current_turn
        self.findChild(QLabel, 'round1Label').setText('Round {}'.format(current_turn + 1))
        self.findChild(QLabel, 'round2Label').setText('Round {}'.format(current_turn + 2))
        self.findChild(QLabel, 'round3Label').setText('Round {}'.format(current_turn + 3))

        spawn_info = self.__game_engine.spawn_information()

        for i, _round in enumerate(spawn_info):
            layout = getattr(self, '_SpawnInfoWidget__round_{}_layout'.format(i + 1))  # type: QVBoxLayout
            box = getattr(self, '_SpawnInfoWidget__round_{}_box'.format(i + 1))  # type: QWidget
            self.__clear_layout(layout)
            for spawn in _round:
                layout.addWidget(UnitSpawnInfoWidget(box, spawn))


    def __clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
