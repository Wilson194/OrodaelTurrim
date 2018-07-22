from PyQt5.QtWidgets import QGraphicsItem, QWidget


class MapTileGraphicsItem(QGraphicsItem):
    def __init__(self, tyle, position):
        super().__init__()
        self.x = x
        self.y = y


    def paint(self, painter, option, widget):
        pixmap = QPixmap(str(Path(__file__).parent / 'res' / 'forest.png'))
        painter.drawPixmap(self.x, self.y, 200, 200, pixmap)


class MapWidget(QWidget):
    pass
