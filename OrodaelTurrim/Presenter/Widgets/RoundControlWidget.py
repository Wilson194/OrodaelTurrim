from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector


class RoundControlWidget(QWidget):

    def __init__(self, parent=None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine

        self.init_ui()


    def init_ui(self):
        with open(str(UI_ROOT / 'roundControlWidget.ui')) as f:
            uic.loadUi(f, self)

        self.findChild(QPushButton, 'endOfRoundButton').clicked.connect(self.end_of_round_slot)
        self.findChild(QPushButton, 'runInferenceButton').clicked.connect(self.run_inference_slot)

        Connector().subscribe('history_action', self.history_state_change_slot)


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
    def history_state_change_slot(self):
        if self.__game_engine.get_game_history():
            self.findChild(QLabel, 'currentRoundLabel').setText(str(self.__game_engine.get_game_history().current_turn))
            self.findChild(QLabel, 'currentPlayerLabel').setText(
                self.__game_engine.get_game_history().active_player.name)

            inference_button = self.findChild(QPushButton, 'runInferenceButton')  # type: QPushButton
            if not self.__game_engine.get_game_history().on_first_player:
                inference_button.setDisabled(True)
            else:
                inference_button.setDisabled(False)
