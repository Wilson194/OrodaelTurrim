import math
from math import sqrt
from pathlib import Path
from typing import List, Tuple, Dict
from PyQt5 import uic
from PyQt5.QtCore import Qt, QRectF, QRect, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QPixmap, QPen, QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QGraphicsScene, QGraphicsView, QScrollArea, QHBoxLayout, \
    QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent, QPushButton
from qtpy import QtGui
from PyQt5 import QtCore
from OrodaelTurrim import IMAGES_ROOT, UI_ROOT, DEBUG, ICONS_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Business.GameMap import GameMap
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Utils import AssetsEncoder
from OrodaelTurrim.Structure.Enums import TerrainType, GameObjectType
from OrodaelTurrim.Structure.GameObjects.GameObject import GameObject
from OrodaelTurrim.Structure.Map import Border
from OrodaelTurrim.Structure.Position import Position, Point

IMAGE_SIZE = Point(296, 200)
HEXAGON_SIZE = Point(296, 148)


class MapTileGraphicsItem(QGraphicsItem):
    """
    Graphic item for render one map tile
    """
    hexagon_offset = Point(149, 127)


    def __init__(self, parent: "MapWidget", map_object: GameMap, position: Position, transformation: float = 0.3):
        """
        Create QGraphicItem object for rendering
        :param map_object: reference to map object
        :param position: position of tile
        :param border: border class for define border rendering
        :param transformation: size multiplication
        """
        super().__init__()
        self.parent = parent
        self.__position = position
        self.__map_object = map_object
        self.__transformation = transformation
        self.__border = None

        self.__calculate_sizes()

        Connector().subscribe('zoom', self.transformation_change_slot)

        # self.setAcceptHoverEvents(True)


    def transformation_change_slot(self, transformation: float):
        self.__transformation = transformation
        self.__calculate_sizes()
        self.update()
        self.parent.scene.update()


    def __calculate_sizes(self):
        self.__image_size = Point(IMAGE_SIZE.x * self.__transformation, IMAGE_SIZE.y * self.__transformation)
        self.__transformation = self.__transformation
        self.__size = HEXAGON_SIZE.x * self.__transformation / 2

        self.__size_w = HEXAGON_SIZE.x * self.__transformation / 2
        self.__size_h = HEXAGON_SIZE.y * self.__transformation / math.sqrt(3)


    def __get_center(self) -> Point:
        """
        Get center of the tile in pixels
        :return: center point
        """
        p = self.__position.axial
        x = self.__size_w * (3. / 2 * p.q)
        y = self.__size_h * ((sqrt(3) / 2 * p.q) + (sqrt(3) * p.r))
        return Point(x, y)


    def __hex_corner_offset(self, corner: int) -> Tuple[float, float]:
        """
        Compute offset to corner
        :param corner: number of corner, start from right corner
        :return: float offset
        """
        angle = math.pi / 180 * (corner * 60)
        return self.__size_w * math.cos(angle), self.__size_h * math.sin(angle)


    def __get_corners(self) -> List[Point]:
        """
        Get list of corners of hexagon
        :return: list of corners points
        """
        center = self.__get_center()
        corners = []
        for i in range(6):
            offset = self.__hex_corner_offset(i)
            corners.append(Point(center.x + offset[0], (center.y + offset[1])))
        return corners


    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        """
        Override paint function. Call every time when need to be render
        :param painter: painter object
        :param option: style options of item
        :param widget: parent widget
        """

        # Get image
        image_path = self.__get_tile_image(self.__map_object[self.__position].terrain_type)
        pixmap = QPixmap(str(image_path))

        painter.drawPixmap(self.boundingRect().toRect(), pixmap)

        # Draw border
        self.__draw_border(painter)

        if DEBUG:
            # Draw position
            self.__draw_position(painter)
            painter.drawRect(self.boundingRect())


    def boundingRect(self) -> QRectF:
        """
        Over rider bounding rectangle for determinate paint event
        :return: rectangle of png image
        """
        center = self.__get_center()

        image_hexagon_diff = (IMAGE_SIZE.y - HEXAGON_SIZE.y) * self.__transformation
        hexagon_width = HEXAGON_SIZE.y * self.__transformation

        left_top = Point(center.x - self.__size, center.y - hexagon_width / 2 - image_hexagon_diff)
        return QRectF(left_top.x,
                      left_top.y,
                      (IMAGE_SIZE.x * self.__transformation),
                      (IMAGE_SIZE.y * self.__transformation))


    def __draw_border(self, painter: QPainter) -> None:
        """
        Draw border based on border definition
        :param painter: painter object
        """
        self.__border = self.parent.borders.get(self.__position, None)

        if not self.__border:
            return

        painter.setOpacity(0.65)

        colors = self.__border.color
        borders = self.__border.order
        corners = self.__get_corners()
        for i in range(len(corners) - 1, -1, -1):
            if borders[i] != 0:
                painter.setPen(QPen(colors[i], borders[i], Qt.SolidLine))

                painter.drawLine(corners[i], corners[i - 1])


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
                         '{},{}'.format(self.__position.offset.q, self.__position.offset.r))


    def __get_tile_image(self, tile_type: TerrainType) -> Path:
        """
        Get path to image based on terrain type
        :param tile_type: enum of terrain type
        :return: Path to png image
        """
        if tile_type == TerrainType.RIVER:
            river_direction = []
            out_of_map_direction = []
            for i, position in enumerate(self.__position.get_all_neighbours()):
                if not self.__map_object.position_on_map(position):
                    out_of_map_direction.append(i)

                elif self.__map_object[position].terrain_type == TerrainType.RIVER:
                    river_direction.append(int(i))

            if out_of_map_direction:
                river_direction.append(
                    sorted(out_of_map_direction, key=lambda x: abs(river_direction[0] - x), reverse=True)[0])

            river_direction.sort()
            return AssetsEncoder['river_{}'.format('-'.join(map(str, river_direction)))]
        else:
            return AssetsEncoder[tile_type]


class ObjectGraphicsItem(QGraphicsItem):
    def __init__(self, parent: "MapWidget", game_engine: GameEngine, position: Position, transformation: float = 0.3):
        """
        Create QGraphicItem object for rendering
        :param map_object: reference to map object
        :param position: position of tile
        :param border: border class for define border rendering
        :param transformation: size multiplication
        """
        super().__init__()
        self.parent = parent
        self.__position = position
        self.__game_engine = game_engine
        self.__transformation = transformation

        Connector().subscribe('zoom', self.transformation_change_slot)

        self.__compute_sizes()
        # self.setAcceptHoverEvents(True)


    def transformation_change_slot(self, transformation: float):
        self.__transformation = transformation
        self.__compute_sizes()
        self.update()
        self.parent.scene.update()


    def __compute_sizes(self):
        self.__image_size = Point(IMAGE_SIZE.x * self.__transformation, IMAGE_SIZE.y * self.__transformation)
        self.__transformation = self.__transformation
        self.__size = HEXAGON_SIZE.x * self.__transformation / 2
        self.__border = None

        self.__size_w = HEXAGON_SIZE.x * self.__transformation / 2
        self.__size_h = HEXAGON_SIZE.y * self.__transformation / math.sqrt(3)


    def __get_center(self) -> Point:
        """
        Get center of the tile in pixels
        :return: center point
        """
        p = self.__position.axial
        x = self.__size_w * (3. / 2 * p.q)
        y = self.__size_h * ((sqrt(3) / 2 * p.q) + (sqrt(3) * p.r))
        return Point(x, y)


    def boundingRect(self) -> QRectF:
        """
        Over rider bounding rectangle for determinate paint event
        :return: rectangle of png image
        """
        center = self.__get_center()

        rect_size = min(self.__size_h, self.__size_w) * 1.6

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

        if self.__game_engine.get_object_type(self.__position) == GameObjectType.NONE:
            return
            # Get image
        image_path = AssetsEncoder[self.__game_engine.get_object_type(self.__position)]
        pixmap = QPixmap(str(image_path))

        painter.drawPixmap(self.boundingRect().toRect(), pixmap)


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
            self.scene.addItem(MapTileGraphicsItem(self, game_map, position, self.transformation))
            self.scene.addItem(ObjectGraphicsItem(self, self.__game_engine, position, self.transformation))

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setCacheMode(QGraphicsView.CacheBackground)
        self.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        # view.setDragMode(QGraphicsView.ScrollHandDrag)

        scroll_layout.addWidget(self.view)
        self.scroll_area.setLayout(scroll_layout)

        zoom_in_button = self.findChild(QPushButton, 'zoomInButton')  # type: QPushButton
        zoom_out_button = self.findChild(QPushButton, 'zoomOutButton')  # type: QPushButton

        zoom_in_button.clicked.connect(self.zoom_in_slot)
        zoom_out_button.clicked.connect(self.zoom_out_slot)

        zoom_out_button.setIcon(QtGui.QIcon(str(ICONS_ROOT / 'zoom_out.png')))
        zoom_in_button.setIcon(QtGui.QIcon(str(ICONS_ROOT / 'zoom_in.png')))
        zoom_out_button.setIconSize(QtCore.QSize(15, 15))
        zoom_in_button.setIconSize(QtCore.QSize(15, 15))

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
        pass
        # self.transformation += 0.1
        # Connector().emit('zoom', self.transformation)
        # self.scene.update()
        # del self.view
        #
        # self.view = QGraphicsView(self.scene)
        # self.view.show()


    @pyqtSlot()
    def zoom_out_slot(self):
        pass
        # self.transformation -= 0.1
        # Connector().emit('zoom', self.transformation)
        #
        # self.scene.update()
        #
        # del self.view
        #
        # self.view = QGraphicsView(self.scene)
        # self.view.show()

        # self.view.setSceneRect(self.view.contentsRect())
