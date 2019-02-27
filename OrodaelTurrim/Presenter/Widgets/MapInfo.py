from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QEvent, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QResizeEvent, QColor
from PyQt5.QtWidgets import QWidget, QGraphicsSceneMouseEvent, QLabel, QTextEdit

from OrodaelTurrim import UI_ROOT, IMAGES_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Utils import AssetsEncoder
from OrodaelTurrim.Structure.Enums import TerrainType
from OrodaelTurrim.Structure.Map import Border
from OrodaelTurrim.Structure.Position import Position


class MapInfoWidget(QWidget):

    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine
        self.__selected_tile = None
        self.label = None

        self.init_ui()


    def init_ui(self):
        with open(str(UI_ROOT / 'mapInfoWidget.ui')) as f:
            uic.loadUi(f, self)

        Connector().subscribe('map_tile_select', self.map_tile_select_slot)

        self.findChild(QLabel, 'tileLabel').setVisible(False)
        self.findChild(QLabel, 'characterLabel').setVisible(False)


    def draw_tile_info(self, position: Position) -> None:
        tile = self.__game_engine.game_map[position]
        tile_type = tile.terrain_type

        img = AssetsEncoder[tile_type]

        label = self.findChild(QLabel, 'tileImageLabel')  # type: QLabel
        label.setScaledContents(True)
        label.setMargin(20)
        label.setPixmap(QPixmap(str(img)).scaled(150, 150, Qt.KeepAspectRatio))

        text = self.findChild(QTextEdit, 'tileInfoText')  # type: QTextEdit
        text.clear()
        text.insertHtml(tile.info_text())

        tile_label = self.findChild(QLabel, 'tileLabel')  # type: QLabel
        tile_label.setVisible(True)
        tile_label.setText('Map tile: {}'.format(tile.__class__.__name__))


    def draw_character_info(self, position: Position):
        if self.__game_engine.is_position_occupied(position):
            character_label = self.findChild(QLabel, 'characterLabel')  # type: QLabel
            character_label.setVisible(True)
            character_label.setContentsMargins(0,0,0,20)
            character_label.setText(
                'Character: {}'.format(self.__game_engine.get_object_type(position).name.capitalize()))

            character_image_label = self.findChild(QLabel, 'characterImageLabel')  # type: QLabel
            character_image_label.setVisible(True)

            img = self.__game_engine.get_object_type(position)

            character_image_label.setPixmap(
                QPixmap(str(AssetsEncoder[img])).scaled(226, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        else:
            self.findChild(QLabel, 'characterLabel').setVisible(False)
            self.findChild(QLabel, 'characterImageLabel').setVisible(False)


    def map_tile_select_slot(self, position: Position):
        self.draw_tile_info(position)
        self.draw_character_info(position)
