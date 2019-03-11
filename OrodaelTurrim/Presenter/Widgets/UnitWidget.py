from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Utils import AssetsEncoder
from OrodaelTurrim.Structure.Enums import GameObjectType
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.GameObjects.Prototypes.Prototype import GameObjectPrototypePool
from OrodaelTurrim.Structure.Position import Position


class UnitWidget(QWidget):
    def __init__(self, parent=None, game_engine: GameEngine = None, object_type: GameObjectType = None):
        super().__init__(parent)

        self.__game_engine = game_engine
        self.__object_type = object_type
        self.__selected_position = None

        Connector().subscribe('map_position_change', self.map_tile_select_slot)
        Connector().subscribe('redraw_ui', self.redraw_ui)
        Connector().subscribe('game_over', self.game_over_slot)

        self.init_ui()


    def init_ui(self):
        with open(str(UI_ROOT / 'unitFrameWidget.ui')) as f:
            uic.loadUi(f, self)

        img = AssetsEncoder[self.__object_type]

        img_label = self.findChild(QLabel, 'imageLabel')  # type: QLabel
        name_label = self.findChild(QLabel, 'nameLabel')  # type: QLabel

        img_label.setScaledContents(True)
        img_label.setPixmap(QPixmap(str(img)))

        name_label.setText(
            '{} ({})'.format(self.__object_type.name.capitalize(), GameObjectPrototypePool[self.__object_type].cost))

        button = self.findChild(QPushButton, 'placeButton')  # type: QPushButton
        button.setDisabled(True)

        self.findChild(QPushButton, 'placeButton').clicked.connect(self.place_unit_slot)


    @pyqtSlot()
    def map_tile_select_slot(self, position: Position):
        self.__selected_position = position
        self.redraw_ui()


    @pyqtSlot()
    def redraw_ui(self):
        state = True

        # Browsing mode
        state = state and self.__game_engine.get_game_history().in_preset

        # Enough money
        player_resources = self.__game_engine.get_resources(self.__game_engine.get_game_history().active_player)
        state = state and GameObjectPrototypePool[self.__object_type].cost <= player_resources

        # Not have a base yet
        base_condition = self.__object_type == GameObjectType.BASE and self.__game_engine.player_have_base(
            self.__game_engine.get_game_history().active_player)
        state = state and not base_condition

        # Position occupation
        state = state and not self.__game_engine.is_position_occupied(self.__selected_position)

        # Game over
        state = state and not Connector().get_variable('game_over')

        self.findChild(QPushButton, 'placeButton').setDisabled(not state)


    @pyqtSlot()
    def place_unit_slot(self):
        player = self.__game_engine.get_game_history().active_player
        unit_info = SpawnInformation(player, self.__object_type, self.__selected_position, [], [])
        self.__game_engine.spawn_unit(unit_info)

        Connector().emit('redraw_map')
        Connector().emit('redraw_ui')


    @pyqtSlot()
    def game_over_slot(self):
        self.redraw_ui()
