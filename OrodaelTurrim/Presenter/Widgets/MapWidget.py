import math
from math import sqrt
from pathlib import Path
from typing import List, Tuple, Dict
from PyQt5 import uic
from PyQt5.QtCore import Qt, QRectF, QRect, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QGraphicsScene, QGraphicsView, QScrollArea, QHBoxLayout, \
    QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent, QPushButton
from qtpy import QtGui
from PyQt5 import QtCore
from OrodaelTurrim import IMAGES_ROOT, UI_ROOT, DEBUG, ICONS_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Utils import AssetsEncoder
from OrodaelTurrim.Structure.Enums import TerrainType, GameObjectType
from OrodaelTurrim.Structure.Map import Border
from OrodaelTurrim.Structure.Position import Position, Point

HEXAGON_SIZE = Point(296, 148)


class GraphicItem(QGraphicsItem):
    image_size = Point(296, 200)
    hexagon_size = HEXAGON_SIZE
    hexagon_offset = Point(149, 127)


    def __init__(self, parent: "MapWidget", game_engine: GameEngine, position: Position, transformation: float = 0.3):
        super().__init__()

        self.parent = parent
        self._position = position
        self._game_engine = game_engine
        self._map_object = game_engine.get_game_map()
        self._transformation = transformation

        self._image_size = None
        self._size = None
        self._size_w = None
        self._size_h = None

        self.calculate_sizes()


    def calculate_sizes(self):
        self._image_size = Point(self.image_size.x * self._transformation, self.image_size.y * self._transformation)
        self._size = self.hexagon_size.x * self._transformation / 2

        self._size_w = self.hexagon_size.x * self._transformation / 2
        self._size_h = self.hexagon_size.y * self._transformation / math.sqrt(3)


    def get_center(self) -> Point:
        """
        Get center of the tile in pixels
        :return: center point
        """
        p = self._position.axial
        x = self._size_w * (3. / 2 * p.q)
        y = self._size_h * ((sqrt(3) / 2 * p.q) + (sqrt(3) * p.r))
        return Point(x, y)


    def hex_corner_offset(self, corner: int) -> Tuple[float, float]:
        """
        Compute offset to corner
        :param corner: number of corner, start from right corner
        :return: float offset
        """
        angle = math.pi / 180 * (corner * 60)
        return self._size_w * math.cos(angle), self._size_h * math.sin(angle)


    def get_corners(self) -> List[Point]:
        """
        Get list of corners of hexagon
        :return: list of corners points
        """
        center = self.get_center()
        corners = []
        for i in range(6):
            offset = self.hex_corner_offset(i)
            corners.append(Point(center.x + offset[0], (center.y + offset[1])))
        return corners


    def boundingRect(self) -> QRectF:
        """
        Over rider bounding rectangle for determinate paint event
        :return: rectangle of png image
        """
        center = self.get_center()

        image_hexagon_diff = (self.image_size.y - self.hexagon_size.y) * self._transformation
        hexagon_width = self.hexagon_size.y * self._transformation

        left_top = Point(center.x - self._size, center.y - hexagon_width / 2 - image_hexagon_diff)
        return QRectF(left_top.x,
                      left_top.y,
                      (self.image_size.x * self._transformation),
                      (self.image_size.y * self._transformation))


class MapTileGraphicsItem(GraphicItem):
    """
    Graphic item for render one map tile
    """


    def __init__(self, parent: "MapWidget", game_engine: GameEngine, position: Position, transformation: float = 0.3):
        """
        Create QGraphicItem object for rendering
        :param map_object: reference to map object
        :param position: position of tile
        :param transformation: size multiplication
        """
        super().__init__(parent, game_engine, position, transformation)

        Connector().subscribe('zoom', self.transformation_change_slot)

        # self.setAcceptHoverEvents(True)


    def transformation_change_slot(self, transformation: float):
        self._transformation = transformation
        self.calculate_sizes()
        self.update()
        self.parent.scene.update()


    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        """
        Override paint function. Call every time when need to be render
        :param painter: painter object
        :param option: style options of item
        :param widget: parent widget
        """

        # Get image
        image_path = self.__get_tile_image(self._map_object[self._position].terrain_type)
        pixmap = QPixmap(str(image_path))

        painter.drawPixmap(self.boundingRect().toRect(), pixmap)

        if DEBUG:
            # Draw test position
            self.__draw_position(painter)
            # Draw image rectangle
            painter.drawRect(self.boundingRect())


    def __draw_position(self, painter: QPainter) -> None:
        """
        Draw offset position to each tile
        """
        font = painter.font()
        font.setPointSize(15)
        painter.setFont(font)
        painter.setPen(QColor(230, 0, 0))

        painter.drawText(self.boundingRect(),
                         Qt.AlignVCenter | Qt.AlignHCenter,
                         '{},{}'.format(self._position.offset.q, self._position.offset.r))


    def __get_tile_image(self, tile_type: TerrainType) -> Path:
        """
        Get path to image based on terrain type
        :param tile_type: enum of terrain type
        :return: Path to png image
        """
        if tile_type == TerrainType.RIVER:
            river_direction = []
            out_of_map_direction = []
            for i, position in enumerate(self._position.get_all_neighbours()):
                if not self._map_object.position_on_map(position):
                    out_of_map_direction.append(i)

                elif self._map_object[position].terrain_type == TerrainType.RIVER:
                    river_direction.append(int(i))

            if out_of_map_direction:
                river_direction.append(
                    sorted(out_of_map_direction, key=lambda x: abs(river_direction[0] - x), reverse=True)[0])

            river_direction.sort()
            return AssetsEncoder['river_{}'.format('-'.join(map(str, river_direction)))]
        else:
            return AssetsEncoder[tile_type]


class ObjectGraphicsItem(GraphicItem):
    def __init__(self, parent: "MapWidget", game_engine: GameEngine, position: Position, transformation: float = 0.3):
        """
        Create QGraphicItem object for rendering
        :param map_object: reference to map object
        :param position: position of tile
        :param border: border class for define border rendering
        :param transformation: size multiplication
        """

        super().__init__(parent, game_engine, position, transformation)

        Connector().subscribe('zoom', self.transformation_change_slot)


    def transformation_change_slot(self, transformation: float):
        self._transformation = transformation
        self.calculate_sizes()
        self.update()
        self.parent.scene.update()


    def boundingRect(self) -> QRectF:
        """
        Over rider bounding rectangle for determinate paint event
        :return: rectangle of png image
        """
        center = self.get_center()

        rect_size = min(self._size_h, self._size_w) * 1.6

        return QRectF(center.x - rect_size / 2,
                      center.y - rect_size / 2,
                      rect_size,
                      rect_size)


    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        """
        Override paint function. Call every time when need to be render
        :param painter: painter object
        :param option: style options of item
        :param widget: parent widget
        """

        # Check if there is object
        if self._game_engine.get_object_type(self._position) == GameObjectType.NONE:
            return

        # Check if object is visible
        if self._position not in self._game_engine.get_player_visible_tiles(
                self._game_engine.get_game_history().active_player):
            return

        image_path = AssetsEncoder[self._game_engine.get_object_type(self._position)]
        pixmap = QPixmap(str(image_path))

        painter.drawPixmap(self.boundingRect().toRect(), pixmap)


class TileBorderGraphicsItem(GraphicItem):

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        border = self.parent.borders.get(self._position, None)

        if not border:
            return

        painter.setOpacity(0.65)

        colors = border.color
        borders = border.order
        corners = self.get_corners()
        for i in range(len(corners) - 1, -1, -1):
            if borders[i] != 0:
                painter.setPen(QPen(colors[i], borders[i], Qt.SolidLine))

                painter.drawLine(corners[i], corners[i - 1])


class TileVisibilityGraphicsItem(GraphicItem):
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        visible = self._position in self._game_engine.get_player_visible_tiles(
            self._game_engine.get_game_history().active_player)

        if not visible:
            painter.setOpacity(0.50)
            painter.setPen(QPen(Qt.white, 0, Qt.SolidLine))

            painter.setBrush(QBrush(QColor(70, 70, 70), Qt.SolidPattern))
            corners = self.get_corners()
            painter.drawConvexPolygon(*corners)


class MapWidget(QWidget):

    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)
        self.__game_engine = game_engine

        self.borders = {}  # type: Dict[Position, Border]

        self.transformation = 0.4

        Connector().subscribe('redraw_map', self.redraw_map)

        self.init_ui()


    def init_ui(self):
        with open(str(UI_ROOT / 'mapWidget.ui')) as f:
            uic.loadUi(f, self)

        self.scroll_area = self.findChild(QScrollArea, 'scrollArea')  # type:QScrollArea
        scroll_layout = QHBoxLayout()

        self.scene = QGraphicsScene(self.scroll_area)

        game_map = self.__game_engine.get_game_map()

        for position in game_map.tiles:
            self.scene.addItem(MapTileGraphicsItem(self, self.__game_engine, position, self.transformation))
            self.scene.addItem(ObjectGraphicsItem(self, self.__game_engine, position, self.transformation))
        for position in game_map.tiles:
            self.scene.addItem(TileVisibilityGraphicsItem(self, self.__game_engine, position, self.transformation))
        for position in game_map.tiles:
            self.scene.addItem(TileBorderGraphicsItem(self, self.__game_engine, position, self.transformation))

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setCacheMode(QGraphicsView.CacheBackground)
        self.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        # view.setDragMode(QGraphicsView.ScrollHandDrag)

        scroll_layout.addWidget(self.view)
        self.scroll_area.setLayout(scroll_layout)

        zoom_in_button = self.findChild(QPushButton, 'zoomInButton')  # type: QPushButton
        zoom_out_button = self.findChild(QPushButton, 'zoomOutButton')  # type: QPushButton
        zoom_reset_button = self.findChild(QPushButton, 'zoomResetButton')  # type: QPushButton

        zoom_in_button.clicked.connect(self.zoom_in_slot)
        zoom_out_button.clicked.connect(self.zoom_out_slot)
        zoom_reset_button.clicked.connect(self.zoom_reset_slot)

        zoom_out_button.setIcon(QtGui.QIcon(str(ICONS_ROOT / 'zoom_out.png')))
        zoom_in_button.setIcon(QtGui.QIcon(str(ICONS_ROOT / 'zoom_in.png')))
        zoom_reset_button.setIcon(QtGui.QIcon(str(ICONS_ROOT / 'zoom_reset.png')))
        zoom_out_button.setIconSize(QtCore.QSize(15, 15))
        zoom_in_button.setIconSize(QtCore.QSize(15, 15))
        zoom_reset_button.setIconSize(QtCore.QSize(15, 15))

        self.scene.mousePressEvent = lambda x: self.click_on_map(x, self.transformation)

        self.view.show()


    @pyqtSlot()
    def click_on_map(self, event: QGraphicsSceneMouseEvent, transformation: float):
        position = Position.from_pixel(event.scenePos(), transformation).offset

        if self.__game_engine.get_game_map().position_on_map(position):
            self.borders.clear()

            self.borders[position] = Border.full(3, QColor(255, 0, 0))
            Connector().emit('map_position_change', position)

        self.scene.update()


    @pyqtSlot()
    def redraw_map(self) -> None:
        print('Redrawing')
        self.scene.update()
        # self.view.update()


    @pyqtSlot()
    def zoom_in_slot(self):
        self.view.scale(1.25, 1.25)


    @pyqtSlot()
    def zoom_out_slot(self):
        self.view.scale(0.80, 0.80)


    @pyqtSlot()
    def zoom_reset_slot(self):
        rect = QtCore.QRectF(self.scene.sceneRect())
        if not rect.isNull():
            self.view.setSceneRect(rect)

            unity = self.view.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
            self.view.scale(1 / unity.width(), 1 / unity.height())
            view_rect = self.view.viewport().rect()
            scene_rect = self.view.transform().mapRect(rect)
            factor = min(view_rect.width() / scene_rect.width(),
                         view_rect.height() / scene_rect.height())
            self.view.scale(factor, factor)
