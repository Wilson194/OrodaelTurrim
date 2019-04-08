import typing
from typing import List, Tuple, Optional

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QPushButton, QListWidget, QListWidgetItem, QAbstractItemView

from OrodaelTurrim import UI_ROOT, ICONS_ROOT
from OrodaelTurrim.Structure.Enums import GameObjectType
from OrodaelTurrim.Structure.Filter.Factory import FilterFactory
from OrodaelTurrim.Structure.Filter.FilterPattern import FilterReference


class ListWidgetItem(QListWidgetItem):
    """ Overload QListWidgetItem for store arguments of the filter"""


    def __init__(self, name: str, arguments: List):
        super().__init__()
        self.name = name
        self.arguments = arguments
        self.setText(name)


class FilterDialog(QDialog):
    """ Window for setup filters and order of the filters"""

    list_widget: QListWidget


    def __init__(self, game_object_type: GameObjectType, filters: List[FilterReference]):
        super().__init__()

        self.game_object_type = game_object_type
        self.filters = filters

        self.init_ui()


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'filterDialog.ui')) as f:
            uic.loadUi(f, self)

        self.list_widget = typing.cast(QListWidget, self.findChild(QListWidget, 'listWidget'))

        add_button = typing.cast(QPushButton, self.findChild(QPushButton, 'addButton'))
        remove_button = typing.cast(QPushButton, self.findChild(QPushButton, 'removeButton'))
        up_button = typing.cast(QPushButton, self.findChild(QPushButton, 'upButton'))
        down_button = typing.cast(QPushButton, self.findChild(QPushButton, 'downButton'))

        # Set images of control buttons
        add_button.setIcon(QIcon(str(ICONS_ROOT / 'plus.png')))
        remove_button.setIcon(QIcon(str(ICONS_ROOT / 'minus.png')))
        up_button.setIcon(QIcon(str(ICONS_ROOT / 'up.png')))
        down_button.setIcon(QIcon(str(ICONS_ROOT / 'down.png')))

        # Connect signals
        add_button.clicked.connect(self.add_filter_slot)
        remove_button.clicked.connect(self.remove_filter_slot)
        up_button.clicked.connect(self.move_filter_up_slot)
        down_button.clicked.connect(self.move_filter_down_slot)

        self.list_widget.setDragDropMode(QAbstractItemView.InternalMove)

        # Load filters based on given list ( saved values)
        for item in self.filters:
            self.list_widget.addItem(ListWidgetItem(item.name, item.arguments))


    @pyqtSlot()
    def add_filter_slot(self) -> None:
        """ Add new filter - spawn new window"""
        result, data = AddFilterDialog.execute_()
        if result:
            self.list_widget.addItem(ListWidgetItem(*data))


    @pyqtSlot()
    def remove_filter_slot(self) -> None:
        """ Remove selected filter """
        for item in self.list_widget.selectedItems():
            self.list_widget.takeItem(self.list_widget.row(item))


    @pyqtSlot()
    def move_filter_up_slot(self) -> None:
        """ Move selected filter up """
        current_row = self.list_widget.currentRow()
        previous_row = current_row - 1

        if previous_row < 0:
            return

        item = self.list_widget.item(current_row)

        self.list_widget.takeItem(current_row)
        self.list_widget.insertItem(previous_row, item)

        self.list_widget.setCurrentRow(previous_row)


    @pyqtSlot()
    def move_filter_down_slot(self) -> None:
        """ Move selected filter down """
        current_row = self.list_widget.currentRow()
        next_row = current_row + 1

        if next_row >= self.list_widget.count():
            return

        item = self.list_widget.item(current_row)

        self.list_widget.takeItem(current_row)
        self.list_widget.insertItem(next_row, item)

        self.list_widget.setCurrentRow(next_row)


    def get_inputs(self) -> List[FilterReference]:
        """ Get inputs from QListWidget"""
        result = []

        item: ListWidgetItem
        for item in self.list_widget.findItems('.*', QtCore.Qt.MatchRegExp):
            result.append(FilterReference(item.name, item.arguments))

        return result


    @staticmethod
    def execute_(game_object_type: GameObjectType, filters: List[FilterReference]):
        dialog = FilterDialog(game_object_type, filters)
        result = dialog.exec_()

        data = dialog.get_inputs()

        return result == QtWidgets.QDialog.Accepted, data


class AddFilterDialog(QDialog):
    """ Add new filter from the list """

    list_widget: QListWidget


    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'addFilterDialog.ui')) as f:
            uic.loadUi(f, self)

        self.list_widget = typing.cast(QListWidget, self.findChild(QListWidget, 'listWidget'))

        self.list_widget.itemDoubleClicked.connect(self.accept)

        # Load filters and set one item for each
        filters = FilterFactory().attack_filters
        for _filter in filters:
            self.list_widget.addItem(_filter.name)


    def get_inputs(self) -> Tuple[Optional[str], List]:
        if self.list_widget.selectedItems():
            selected = self.list_widget.selectedItems()[0]  # type: QListWidgetItem
            return selected.text(), []

        return None, []


    @staticmethod
    def execute_():
        dialog = AddFilterDialog()
        result = dialog.exec_()

        data = dialog.get_inputs()

        if data[0] is None:
            return False, (None, [])
        return result == QtWidgets.QDialog.Accepted, data
