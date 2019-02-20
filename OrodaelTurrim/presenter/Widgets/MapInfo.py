from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QEvent, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QResizeEvent, QColor
from PyQt5.QtWidgets import QWidget, QGraphicsSceneMouseEvent, QLabel, QTextEdit

from OrodaelTurrim import UI_ROOT, IMAGES_ROOT
from OrodaelTurrim.business.GameEngine import GameEngine
from OrodaelTurrim.presenter.Connector import Connector
from OrodaelTurrim.structure.Enums import TerrainType
from OrodaelTurrim.structure.Map import Border
from OrodaelTurrim.structure.Position import Position


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


    def draw_tile_info(self, position: Position):
        tile = self.__game_engine.game_map[position]
        tile_type = tile.terrain_type

        if tile_type == TerrainType.FIELD:
            img = IMAGES_ROOT / 'field.png'

        elif tile_type == TerrainType.FOREST:
            img = IMAGES_ROOT / 'forest.png'

        elif tile_type == TerrainType.HILL:
            img = IMAGES_ROOT / 'hill.png'

        elif tile_type == TerrainType.MOUNTAIN:
            img = IMAGES_ROOT / 'mountain.png'

        elif tile_type == TerrainType.VILLAGE:
            img = IMAGES_ROOT / 'village.png'
        else:
            img = IMAGES_ROOT / 'river_0-2.png'

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
        self.findChild(QLabel, 'characterLabel').setVisible(True)


    def map_tile_select_slot(self, position: Position):
        self.draw_tile_info(position)
        self.draw_character_info(position)
