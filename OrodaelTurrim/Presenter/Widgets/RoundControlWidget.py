from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QSpinBox, QCheckBox

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector


class RoundControlWidget(QWidget):

    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine

        self.init_ui()

        Connector().subscribe('redraw_ui', self.redraw_ui)


    def init_ui(self):
        with open(str(UI_ROOT / 'roundControlWidget.ui')) as f:
            uic.loadUi(f, self)

        self.findChild(QPushButton, 'endOfRoundButton').clicked.connect(self.end_of_round_slot)
        self.findChild(QPushButton, 'runInferenceButton').clicked.connect(self.run_inference_slot)

        self.findChild(QPushButton, 'playButton').clicked.connect(self.simulate_game_slot)

        self.findChild(QPushButton, 'previousTurnButton').clicked.connect(self.previous_turn_slot)
        self.findChild(QPushButton, 'nextTurnButton').clicked.connect(self.next_turn_slot)
        self.findChild(QPushButton, 'lastTurnButton').clicked.connect(self.last_turn_slot)

        self.findChild(QPushButton, 'nextTurnButton').setDisabled(True)
        self.findChild(QPushButton, 'lastTurnButton').setDisabled(True)


    @pyqtSlot()
    def end_of_round_slot(self):
        game_history = self.__game_engine.get_game_history()

        current_player = self.__game_engine.get_player(game_history.current_player)

        self.__game_engine.simulate_rest_of_player_turn(current_player)
        Connector().functor('redraw_map')()

        while not game_history.on_first_player:
            game_history.active_player.act()
            self.__game_engine.simulate_rest_of_player_turn(game_history.active_player)


    @pyqtSlot()
    def run_inference_slot(self):
        if self.__game_engine.get_game_history().on_first_player:
            self.__game_engine.get_game_history().active_player.act()


    @pyqtSlot()
    def redraw_ui(self):
        if self.__game_engine.get_game_history():
            self.findChild(QLabel, 'currentRoundLabel').setText(str(self.__game_engine.get_game_history().current_turn))
            self.findChild(QLabel, 'currentPlayerLabel').setText(
                self.__game_engine.get_game_history().active_player.name)

            inference_button = self.findChild(QPushButton, 'runInferenceButton')  # type: QPushButton
            end_of_round_button = self.findChild(QPushButton, 'endOfRoundButton')  # type: QPushButton
            play_button = self.findChild(QPushButton, 'playButton')  # type: QPushButton

            if not self.__game_engine.get_game_history().in_preset:
                end_of_round_button.setDisabled(True)
                play_button.setDisabled(True)
            else:
                end_of_round_button.setDisabled(False)
                play_button.setDisabled(False)

            if self.__game_engine.get_game_history().on_first_player and self.__game_engine.get_game_history().in_preset:
                inference_button.setDisabled(False)
            else:
                inference_button.setDisabled(True)


    @pyqtSlot()
    def simulate_game_slot(self):
        rounds_box = self.findChild(QSpinBox, 'roundsBox')  # type: QSpinBox
        rounds = rounds_box.value()

        check_box = self.findChild(QCheckBox, 'displayProcessCheck')  # type: QCheckBox
        display = check_box.isChecked()

        game_history = self.__game_engine.get_game_history()
        while rounds > 0:
            game_history.active_player.act()
            self.__game_engine.simulate_rest_of_player_turn(game_history.active_player)

            if display:
                Connector().emit('redraw_map')

            if game_history.on_first_player:
                rounds -= 1

        Connector().emit('redraw_map')


    @pyqtSlot()
    def previous_turn_slot(self):
        self.__game_engine.get_game_history().move_turn_back()

        self.findChild(QPushButton, 'nextTurnButton').setDisabled(False)
        self.findChild(QPushButton, 'lastTurnButton').setDisabled(False)


    @pyqtSlot()
    def next_turn_slot(self):
        self.__game_engine.get_game_history().move_turn_forth()

        if self.__game_engine.get_game_history().in_preset:
            self.findChild(QPushButton, 'nextTurnButton').setDisabled(True)
            self.findChild(QPushButton, 'lastTurnButton').setDisabled(True)


    @pyqtSlot()
    def last_turn_slot(self):
        self.__game_engine.get_game_history().move_to_present()
