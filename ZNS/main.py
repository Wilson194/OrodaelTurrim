from PyQt5.QtCore import qrand, qsrand
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QGraphicsItem, QApplication, QGraphicsScene, QGraphicsView
import typing
from pathlib import Path


class MapTileGraphicsItem(QGraphicsItem):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y


    def paint(self, painter, option, widget):
        pixmap = QPixmap(str(Path(__file__).parent / 'res' / 'forest.png'))
        painter.drawPixmap(self.x, self.y, 200, 200, pixmap)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    scene = QGraphicsScene()
    scene.setSceneRect(-200, -200, 600, 600)
    scene.setItemIndexMethod(QGraphicsScene.NoIndex)

    tile = MapTile(0, -145)
    scene.addItem(tile)

    tile = MapTile(0,0)
    scene.addItem(tile)



    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.Antialiasing)
    view.setCacheMode(QGraphicsView.CacheBackground)
    view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
    # view.setDragMode(QGraphicsView.ScrollHandDrag)
    view.setWindowTitle("Colliding Mice")
    view.resize(400, 300)
    view.show()

    sys.exit(app.exec_())
