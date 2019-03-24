from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QEvent, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QResizeEvent, QColor
from PyQt5.QtWidgets import QWidget, QGraphicsSceneMouseEvent, QLabel, QTextEdit

from OrodaelTurrim import UI_ROOT, IMAGES_ROOT, ICONS_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Utils import AssetsEncoder
from OrodaelTurrim.Structure.Position import Position


class MapInfoWidget(QWidget):

    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine
        self.__selected_tile = None
        self.label = None

        Connector().subscribe('map_position_change', self.map_tile_select_slot)
        Connector().subscribe('redraw_ui', self.redraw_ui_slot)

        self.init_ui()


    def init_ui(self):
        with open(str(UI_ROOT / 'mapInfoWidget.ui')) as f:
            uic.loadUi(f, self)

        self.findChild(QLabel, 'tileLabel').setVisible(False)
        self.findChild(QLabel, 'characterLabel').setVisible(False)

        self.findChild(QLabel, 'positionLabel').setVisible(False)
        self.findChild(QLabel, 'positionLabel').setContentsMargins(0, 0, 0, 60)

        self.findChild(QLabel, 'offsetPositionLabel').setVisible(False)
        self.findChild(QLabel, 'cubicPositionLabel').setVisible(False)
        self.findChild(QLabel, 'axialPositionLabel').setVisible(False)

        offset_icon = self.findChild(QLabel, 'offsetIconLabel')  # type: QLabel
        cubic_icon = self.findChild(QLabel, 'cubicIconLabel')  # type: QLabel
        axial_icon = self.findChild(QLabel, 'axialIconLabel')  # type: QLabel

        offset_icon.setScaledContents(True)
        offset_icon.setVisible(False)
        offset_icon.setPixmap(QPixmap(str(ICONS_ROOT / 'offset.png')))

        cubic_icon.setScaledContents(True)
        cubic_icon.setVisible(False)
        cubic_icon.setPixmap(QPixmap(str(ICONS_ROOT / 'cube.png')))

        axial_icon.setScaledContents(True)
        axial_icon.setVisible(False)
        axial_icon.setPixmap(QPixmap(str(ICONS_ROOT / 'axis.png')))


    def draw_tile_info(self, position: Position) -> None:
        if position:
            tile = self.__game_engine.get_game_map()[position]
            tile_type = tile.terrain_type

            img = AssetsEncoder[tile_type]

            label = self.findChild(QLabel, 'tileImageLabel')  # type: QLabel
            label.setVisible(True)
            label.setScaledContents(True)
            label.setMargin(20)
            label.setPixmap(QPixmap(str(img)).scaled(150, 150, Qt.KeepAspectRatio))

            text = self.findChild(QTextEdit, 'tileInfoText')  # type: QTextEdit
            text.setVisible(True)
            text.clear()
            text.insertHtml(tile.info_text())

            tile_label = self.findChild(QLabel, 'tileLabel')  # type: QLabel
            tile_label.setVisible(True)
            tile_label.setText('Map tile: {}'.format(tile.__class__.__name__))
        else:
            self.findChild(QLabel, 'tileImageLabel').setVisible(False)
            self.findChild(QTextEdit, 'tileInfoText').setText('')
            self.findChild(QLabel, 'tileLabel').setVisible(False)


    def draw_character_info(self, position: Position):
        if position and self.__game_engine.is_position_occupied(position):
            character_label = self.findChild(QLabel, 'characterLabel')  # type: QLabel
            character_label.setVisible(True)
            character_label.setContentsMargins(0, 0, 0, 20)
            character_label.setText(
                'Character: {}'.format(self.__game_engine.get_object_type(position).name.capitalize()))

            character_image_label = self.findChild(QLabel, 'characterImageLabel')  # type: QLabel
            character_image_label.setVisible(True)

            img = self.__game_engine.get_object_type(position)

            character_image_label.setPixmap(
                QPixmap(str(AssetsEncoder[img])).scaled(226, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            self.findChild(QTextEdit, 'characterInfoWidget').setText(
                self.__game_engine.get_game_object(position).description)

        else:
            self.findChild(QLabel, 'characterLabel').setVisible(False)
            self.findChild(QLabel, 'characterImageLabel').setVisible(False)
            self.findChild(QTextEdit, 'characterInfoWidget').setText('')


    def draw_character_effects(self):
        text_edit = self.findChild(QTextEdit, 'characterEffectsText')  # type: QTextEdit
        text = ''
        if self.__selected_tile and self.__game_engine.is_position_occupied(self.__selected_tile):
            effects = self.__game_engine.get_game_object(self.__selected_tile).active_effects
            for effect in effects:
                text += '<p>{} ({})</p>'.format(effect.effect_type.name.capitalize(), effect.remaining_duration)

        text_edit.setText(text)


    def draw_position_info(self, position: Position) -> None:
        if position:
            offset_icon = self.findChild(QLabel, 'offsetPositionLabel')  # type: QLabel
            cubic_icon = self.findChild(QLabel, 'cubicPositionLabel')  # type: QLabel
            axial_icon = self.findChild(QLabel, 'axialPositionLabel')  # type: QLabel

            self.findChild(QLabel, 'offsetIconLabel').setVisible(True)
            self.findChild(QLabel, 'cubicIconLabel').setVisible(True)
            self.findChild(QLabel, 'axialIconLabel').setVisible(True)
            self.findChild(QLabel, 'positionLabel').setVisible(True)

            offset_icon.setVisible(True)
            offset_icon.setText(position.offset.string)

            cubic_icon.setVisible(True)
            cubic_icon.setText(position.cubic.string)

            axial_icon.setVisible(True)
            axial_icon.setText(position.axial.string)
        else:
            self.findChild(QLabel, 'offsetIconLabel').setVisible(False)
            self.findChild(QLabel, 'cubicIconLabel').setVisible(False)
            self.findChild(QLabel, 'axialIconLabel').setVisible(False)
            self.findChild(QLabel, 'positionLabel').setVisible(False)
            self.findChild(QLabel, 'offsetPositionLabel').setVisible(False)
            self.findChild(QLabel, 'cubicPositionLabel').setVisible(False)
            self.findChild(QLabel, 'axialPositionLabel').setVisible(False)


    def redraw_ui_slot(self):
        self.draw_tile_info(self.__selected_tile)
        self.draw_character_info(self.__selected_tile)
        self.draw_position_info(self.__selected_tile)
        self.draw_character_effects()


    def map_tile_select_slot(self, position: Position) -> None:
        self.__selected_tile = position
        self.redraw_ui_slot()
