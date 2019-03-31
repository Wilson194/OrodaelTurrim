from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QEvent, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QResizeEvent, QColor, QIcon
from PyQt5.QtWidgets import QWidget, QGraphicsSceneMouseEvent, QLabel, QTextEdit, QPushButton

from OrodaelTurrim import UI_ROOT, IMAGES_ROOT, ICONS_ROOT
from OrodaelTurrim.Business.Factory import BorderFactory
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Utils import AssetsEncoder
from OrodaelTurrim.Structure.Enums import AttributeType, GameRole
from OrodaelTurrim.Structure.Map import Border
from OrodaelTurrim.Structure.Position import Position


class MapInfoWidget(QWidget):

    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine
        self.__selected_tile = None
        self.label = None

        Connector().subscribe('map_position_change', self.map_tile_select_slot)
        Connector().subscribe('redraw_ui', self.redraw_ui_slot)
        Connector().subscribe('game_thread_finished', self.redraw_ui_slot)

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

        visibility_button = self.findChild(QPushButton, 'visibilityButton')  # type: QPushButton
        attack_button = self.findChild(QPushButton, 'attackButton')  # type: QPushButton
        move_button = self.findChild(QPushButton, 'moveButton')  # type: QPushButton

        visibility_button.setIcon(QIcon(str(ICONS_ROOT / 'eye.png')))
        visibility_button.clicked.connect(self.show_visibility_slot)
        visibility_button.setVisible(False)

        attack_button.setIcon(QIcon(str(ICONS_ROOT / 'sword.png')))
        attack_button.clicked.connect(self.show_attack_range_slot)
        attack_button.setVisible(False)

        move_button.setIcon(QIcon(str(ICONS_ROOT / 'foot.png')))
        move_button.clicked.connect(self.show_accessible_tiles_slot)
        move_button.setVisible(False)

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


    def draw_character_info(self, position: Position):  # TODO: Refactor add hide not visible unit
        if position and self.__game_engine.is_position_occupied(position):
            # Display name of the game object
            character_label = self.findChild(QLabel, 'characterLabel')  # type: QLabel
            character_label.setVisible(True)
            character_label.setContentsMargins(0, 0, 0, 20)
            character_label.setText(
                'Character: {}'.format(self.__game_engine.get_object_type(position).name.capitalize()))

            # Display game object image
            character_image_label = self.findChild(QLabel, 'characterImageLabel')  # type: QLabel
            character_image_label.setVisible(True)

            img = self.__game_engine.get_object_type(position)

            character_image_label.setPixmap(
                QPixmap(str(AssetsEncoder[img])).scaled(226, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            # Unit attributes
            self.findChild(QTextEdit, 'objectAttributesText').setText(
                self.__game_engine.get_game_object(position).description)

            # Display unit filters
            if self.__game_engine.get_game_object(position).role == GameRole.DEFENDER:
                attack_filters = self.__game_engine.get_game_object(position).attack_filters
                text = ''
                for attack_filter in attack_filters:
                    text += '{} <br>'.format(attack_filter.__class__.__name__)
                text += 'Random'
                self.findChild(QLabel, 'objectFiltersLabel').setVisible(True)
                self.findChild(QTextEdit, 'objectFiltersText').setText(text)
            else:
                self.findChild(QTextEdit, 'objectFiltersText').setText('')
                self.findChild(QLabel, 'objectFiltersLabel').setVisible(False)

            self.findChild(QPushButton, 'visibilityButton').setVisible(True)
            self.findChild(QPushButton, 'attackButton').setVisible(True)
            self.findChild(QPushButton, 'moveButton').setVisible(True)

            self.findChild(QLabel, 'objectAttributesLabel').setVisible(True)
            self.findChild(QLabel, 'objectEffectsLabel').setVisible(True)


        else:
            self.findChild(QLabel, 'characterLabel').setVisible(False)
            self.findChild(QLabel, 'characterImageLabel').setVisible(False)
            self.findChild(QTextEdit, 'objectAttributesText').setText('')

            self.findChild(QLabel, 'objectAttributesLabel').setVisible(False)
            self.findChild(QLabel, 'objectEffectsLabel').setVisible(False)
            self.findChild(QLabel, 'objectFiltersLabel').setVisible(False)

            self.findChild(QPushButton, 'visibilityButton').setVisible(False)
            self.findChild(QPushButton, 'attackButton').setVisible(False)
            self.findChild(QPushButton, 'moveButton').setVisible(False)


    def draw_character_effects(self):
        text_edit = self.findChild(QTextEdit, 'objectEffectsText')  # type: QTextEdit
        text = ''
        if self.__selected_tile and self.__game_engine.is_position_occupied(self.__selected_tile):
            effects = self.__game_engine.get_game_object(self.__selected_tile).active_effects
            for effect in effects:
                text += '{} ({})<br>'.format(effect.effect_type.name.capitalize(), effect.remaining_duration)

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


    @pyqtSlot(Position)
    def map_tile_select_slot(self, position: Position) -> None:
        self.__selected_tile = position
        self.redraw_ui_slot()


    @pyqtSlot()
    def show_visibility_slot(self):
        tiles = self.__game_engine.get_game_object(self.__selected_tile).visible_tiles

        border_dict = BorderFactory.create(3, QColor(0, 0, 255), tiles)

        Connector().emit('display_border', border_dict, [QColor(0, 0, 255)])


    @pyqtSlot()
    def show_attack_range_slot(self):
        attack_range = self.__game_engine.get_game_object(self.__selected_tile).get_attribute(
            AttributeType.ATTACK_RANGE)

        tiles = self.__game_engine.get_game_map().get_visible_tiles(self.__selected_tile, attack_range)

        border_dict = BorderFactory.create(3, QColor(0, 0, 255), tiles)

        Connector().emit('display_border', border_dict, [QColor(0, 0, 255)])


    @pyqtSlot()
    def show_accessible_tiles_slot(self):
        tiles = self.__game_engine.get_game_object(self.__selected_tile).accessible_tiles

        border_dict = BorderFactory.create(3, QColor(0, 0, 255), tiles)

        Connector().emit('display_border', border_dict, [QColor(0, 0, 255)])
