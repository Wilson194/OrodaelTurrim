import inspect
from typing import Union, List

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QPushButton, QListWidget, QListWidgetItem, QAbstractItemView
from OrodaelTurrim.Structure.Filter import AttackFilter
from OrodaelTurrim.Structure.Filter.Factory import FilterFactory
from OrodaelTurrim.Structure.Filter.FilterPattern import AttackFilter as AttackFilterPattern, FilterReference

from OrodaelTurrim import UI_ROOT, ICONS_ROOT
from OrodaelTurrim.Structure.Enums import GameObjectType


class ListWidgetItem(QListWidgetItem):
    def __init__(self, name, arguments):
        super().__init__()
        self.name = name
        self.arguments = arguments
        self.setText(name)


class FilterDialog(QDialog):

    def __init__(self, game_object_type: GameObjectType, filters: List[FilterReference]):
        super().__init__()

        self.__game_object_type = game_object_type
        self.__filters = filters

        self.__list = None

        self.init_ui()


    def init_ui(self):
        with open(str(UI_ROOT / 'filterDialog.ui')) as f:
            uic.loadUi(f, self)

        self.__list = self.findChild(QListWidget, 'listWidget')  # type: QListWidget

        add_button: QPushButton = self.findChild(QPushButton, 'addButton')
        remove_button = self.findChild(QPushButton, 'removeButton')  # type: QPushButton
        up_button = self.findChild(QPushButton, 'upButton')  # type: QPushButton
        down_button = self.findChild(QPushButton, 'downButton')  # type: QPushButton

        add_button.setIcon(QIcon(str(ICONS_ROOT / 'plus.png')))
        remove_button.setIcon(QIcon(str(ICONS_ROOT / 'minus.png')))
        up_button.setIcon(QIcon(str(ICONS_ROOT / 'up.png')))
        down_button.setIcon(QIcon(str(ICONS_ROOT / 'down.png')))

        add_button.clicked.connect(self.add_filter_slot)
        remove_button.clicked.connect(self.remove_filter_slot)
        up_button.clicked.connect(self.move_filter_up_slot)
        down_button.clicked.connect(self.move_filter_down_slot)

        self.__list.setDragDropMode(QAbstractItemView.InternalMove)

        for item in self.__filters:
            self.__list.addItem(ListWidgetItem(item.name, item.arguments))


    @pyqtSlot()
    def add_filter_slot(self):
        result, data = AddFilterDialog.execute_()
        if result:
            self.__list.addItem(ListWidgetItem(*data))


    @pyqtSlot()
    def remove_filter_slot(self):
        for item in self.__list.selectedItems():
            self.__list.takeItem(self.__list.row(item))


    @pyqtSlot()
    def move_filter_up_slot(self):
        current_row = self.__list.currentRow()
        previous_row = current_row - 1

        if previous_row < 0:
            return

        item = self.__list.item(current_row)

        self.__list.takeItem(current_row)
        self.__list.insertItem(previous_row, item)

        self.__list.setCurrentRow(previous_row)


    @pyqtSlot()
    def move_filter_down_slot(self):
        current_row = self.__list.currentRow()
        next_row = current_row + 1

        if next_row >= self.__list.count():
            return

        item = self.__list.item(current_row)

        self.__list.takeItem(current_row)
        self.__list.insertItem(next_row, item)

        self.__list.setCurrentRow(next_row)


    def get_inputs(self):
        result = []
        for item in self.__list.findItems('.*', QtCore.Qt.MatchRegExp):
            result.append(FilterReference(item.name, item.arguments))

        return result


    @staticmethod
    def execute_(game_object_type: GameObjectType, filters: List[FilterReference]):
        dialog = FilterDialog(game_object_type, filters)
        result = dialog.exec_()

        data = dialog.get_inputs()

        return result == QtWidgets.QDialog.Accepted, data


class AddFilterDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.list_widget = None  # type: QListWidget

        self.init_ui()


    def init_ui(self):
        with open(str(UI_ROOT / 'addFilterDialog.ui')) as f:
            uic.loadUi(f, self)

        self.list_widget = self.findChild(QListWidget, 'listWidget')

        self.list_widget.itemDoubleClicked.connect(self.accept)

        filters = FilterFactory().attack_filters
        for _filter in filters:
            self.list_widget.addItem(_filter.name)


    def get_list_of_filters(self):
        result = []
        for name, obj, in inspect.getmembers(AttackFilter):
            if inspect.isclass(obj) and issubclass(obj, AttackFilterPattern) and not inspect.isabstract(obj):
                parameters = [parameter for parameter in inspect.getfullargspec(obj.__init__).args if
                              parameter not in ['self', 'map_proxy', 'game_object_proxy']]
                result.append((name, parameters))

        return result


    def get_inputs(self):
        selected = self.list_widget.selectedItems()[0]  # type: QListWidgetItem
        return selected.text(), []


    @staticmethod
    def execute_():
        dialog = AddFilterDialog()
        result = dialog.exec_()

        data = dialog.get_inputs()

        return result == QtWidgets.QDialog.Accepted, data
