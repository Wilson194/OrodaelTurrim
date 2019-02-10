import math
from math import sqrt
from pathlib import Path
from typing import List, Tuple
from PyQt5 import uic
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPen
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QGraphicsScene, QGraphicsView, QScrollArea, QHBoxLayout, \
    QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent

from OrodaelTurrim import IMAGES_ROOT, UI_ROOT
from OrodaelTurrim.business.GameEngine import GameEngine
from OrodaelTurrim.business.GameMap import GameMap
from OrodaelTurrim.structure.Enums import TerrainType
from OrodaelTurrim.structure.Position import Position, Point, Border, CubicPosition


class MapTileGraphicsItem(QGraphicsItem):
    """
    Graphic item for render one map tile
    """
    image_size = Point(296, 195)
    hexagon_offset = Point(149, 127)

    def __init__(self, map_object: GameMap, position: Position, border: Border, size: float = 0.3):
        """
        Create QGraphicItem object for rendering
        :param map_object: reference to map object
        :param position: position of tile
        :param border: border class for define border rendering
        :param size: size multiplication
        """
        super().__init__()
        self.__position = position
        self.__map_object = map_object
        self.__tile_size = Point(self.image_size.x * size, self.image_size.y * size)
        self.__size = size
        self.__border = border
        # self.setAcceptHoverEvents(True)

    def __get_center(self) -> Point:
        """
        Get center of the tile in pixels
        :return: center point
        """
        p = self.__position.axial
        x = self.__tile_size.x / 2 * (3 / 2 * p.q)
        y = self.__tile_size.y / 2 * (sqrt(3) / 2 * p.q + sqrt(3) * p.r)
        return Point(x, y)

    def __hex_corner_offset(self, corner: int) -> Tuple[float, float]:
        """
        Compute offset to corner
        :param corner: number of corner, start from right corner
        :return: float offset
        """
        angle = 2 * math.pi * corner / 6
        return self.__tile_size.x / 2 * math.cos(angle), self.__tile_size.y / 2 * math.sin((angle))

    def __get_corners(self) -> List[Point]:
        """
        Get list of corners of hexagon
        :return: list of corners points
        """
        center = self.__get_center()
        corners = []
        for i in range(6):
            offset = self.__hex_corner_offset(i)
            corners.append(Point(
                center.x + offset[0],
                (center.y + offset[1]) * sqrt(3) / 2
            ))
        return corners

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        """
        Override paint function. Call every time when need to be render
        :param painter: painter object
        :param option: style options of item
        :param widget: parent widget
        """

        # Get image
        image_path = self.__get_tile_image(self.__map_object[self.__position].get_type())
        pixmap = QPixmap(str(image_path))

        # Draw image
        center = self.__get_center()
        painter.drawPixmap(center.x, center.y * sqrt(3) / 2, self.__tile_size.x, self.__tile_size.y + 5, pixmap)

        # Draw border
        self.__draw_border(painter)

        # Draw position
        self.__draw_position(painter)

        painter.drawRect(self.boundingRect())

        painter.drawEllipse(self.__get_center()*Point(1., sqrt(3) / 2), 3, 3)

    def boundingRect(self) -> QRectF:
        """
        Over rider bounding rectangle for determinate paint event
        :return: rectangle of png image
        """
        center = self.__get_center()

        center *= Point(1., sqrt(3) / 2)
        return QRectF(center.QPointF, (center + self.image_size * self.__size).QPointF)

    def __draw_border(self, painter: QPainter) -> None:
        """
        Draw border based on border definition
        :param painter: painter object
        """
        colors = self.__border.color
        borders = self.__border.order
        corners = self.__get_corners()
        for i in range(len(corners) - 1, -1, -1):
            if borders[i] != 0:
                painter.setPen(QPen(colors[i], borders[i], Qt.SolidLine))

                painter.drawLine(corners[i] + (self.hexagon_offset * self.__size),
                                 corners[i - 1] + (self.hexagon_offset * self.__size))

    def __draw_position(self, painter: QPainter) -> None:
        painter.drawText(self.boundingRect(),
                         Qt.AlignVCenter | Qt.AlignHCenter,
                         '{},{}'.format(self.__position.offset.q, self.__position.offset.r))

    def __get_tile_image(self, tile_type: TerrainType) -> Path:
        """
        Get path to image based on terrain type
        :param tile_type: enum of terrain type
        :return: Path to png image
        """
        if tile_type == TerrainType.FIELD:
            return IMAGES_ROOT / 'field.png'

        elif tile_type == TerrainType.FOREST:
            return IMAGES_ROOT / 'forest.png'

        elif tile_type == TerrainType.HILL:
            return IMAGES_ROOT / 'hill.png'

        elif tile_type == TerrainType.MOUNTAIN:
            return IMAGES_ROOT / 'mountain.png'

        elif tile_type == TerrainType.VILLAGE:
            return IMAGES_ROOT / 'village.png'
        else:
            river_direction = []
            out_of_map_direction = []
            for i, position in enumerate(self.__position.get_all_neighbours()):
                if not self.__map_object.position_on_map(position):
                    out_of_map_direction.append(i)

                elif self.__map_object[position].get_type() == TerrainType.RIVER:
                    river_direction.append(int(i))

            if out_of_map_direction:
                river_direction.append(
                    sorted(out_of_map_direction, key=lambda x: abs(river_direction[0] - x), reverse=True)[0])

            river_direction.sort()
            return IMAGES_ROOT / 'river_{}.png'.format('-'.join(map(str, river_direction)))


class MapWidget(QWidget):
    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)
        self.__game_engine = game_engine

        with open(str(UI_ROOT / 'mapWidget.ui')) as f:
            uic.loadUi(f, self)

        self.scroll_area = self.findChild(QScrollArea, 'scrollArea')
        scroll_layout = QHBoxLayout()

        self.scene = QGraphicsScene()
        # scene.setSceneRect(0, 0, 600, 600)
        # scene.setItemIndexMethod(QGraphicsScene.NoIndex)

        game_map = self.__game_engine.game_map

        for tile in game_map.tiles:
            self.scene.addItem(MapTileGraphicsItem(game_map, tile, Border()))

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setCacheMode(QGraphicsView.CacheBackground)
        self.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        # view.setDragMode(QGraphicsView.ScrollHandDrag)
        # view.resize(400, 300)

        scroll_layout.addWidget(self.view)
        self.scroll_area.setLayout(scroll_layout)

        self.scene.mousePressEvent = self.click_on_map

        self.view.show()

    def click_on_map(self, event: 'QGraphicsSceneMouseEvent'):
        # print(Position.from_pixel(event.pos()).offset)
        # print('scene', event.scenePos())
        print(event.scenePos())
        print('-' * 50)
