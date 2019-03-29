from typing import List, TYPE_CHECKING
from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Structure.Enums import GameRole
from OrodaelTurrim.Structure.Exceptions import IllegalHistoryOperation

if TYPE_CHECKING:
    from OrodaelTurrim.Structure.Actions.Abstract import GameAction


class GameHistory:
    def __init__(self, turn_limit: int, players: List[IPlayer]):
        self.__turn_limit = turn_limit
        self.__players = players

        self.__current_turn = -1
        self.__current_player = 0
        self.__current_action = -1

        self.__turns = []  # type: List[List[List["GameAction"]]]

        self.__log_signal = Connector().functor('update_log')

        self.start_next_game_turn()


    def start_next_game_turn(self) -> None:
        self.__current_turn += 1
        self.__current_player = -1

        self.__turns.append([])
        self.start_next_player_turn()

        Connector().functor('redraw_ui')()


    def start_next_player_turn(self) -> None:
        self.__current_player += 1
        self.__current_action = -1

        self.__turns[self.__current_turn].append([])

        Connector().functor('redraw_ui')()


    def delete_player_turn(self) -> None:
        self.__turns[self.__current_turn].pop(self.__current_player)


    def delete_game_turn(self) -> None:
        self.__turns.pop(self.__current_turn)


    def redo_player_actions(self) -> None:
        if self.before_first_action:
            self.move_to_next()

        player_actions = self.__turns[self.__current_turn][self.__current_player]

        while self.__current_action <= self.last_action_index:
            player_actions[self.__current_action].execute()

            self.__current_action += 1

        self.__current_action = self.last_action_index


    def undo_player_actions(self) -> None:
        player_actions = self.__turns[self.__current_turn][self.__current_player]
        while self.__current_action >= 0:
            player_actions[self.__current_action].undo()
            self.__current_action -= 1


    def clear_player_turn(self) -> None:
        self.__turns[self.__current_turn][self.__current_player].clear()


    def move_to_next(self) -> None:
        if self.in_preset:
            return

        if not self.on_last_action:
            self.__current_action += 1
            return
        else:
            self.__current_action = -1

        if not self.on_last_player:
            self.__current_player += 1
            return
        else:
            self.__current_player = 0

        self.__current_turn += 1

        Connector().functor('redraw_ui')()


    def move_to_previous(self) -> None:
        if self.at_start:
            return

        if not self.before_first_action:
            self.__current_action -= 1
            return

        if not self.on_first_player:
            self.__current_player -= 1
        else:
            self.__current_player = len(self.__players) - 1
            self.__current_turn -= 1

        self.__current_action = self.last_action_index

        Connector().functor('redraw_ui')()


    @property
    def current_action(self) -> "GameAction":
        if self.before_first_action:
            raise IllegalHistoryOperation('Cannot access action - action pointer is before first action!')

        return self.__turns[self.__current_turn][self.__current_player][self.__current_action]


    @property
    def last_action_index(self) -> int:
        return len(self.__turns[self.__current_turn][self.__current_player]) - 1


    @property
    def on_present_turn(self) -> bool:
        return self.__current_turn == (len(self.__turns) - 1)


    @property
    def on_first_player(self) -> bool:
        return self.__current_player == 0


    @property
    def on_present_player(self) -> bool:
        return self.__current_player == (len(self.__turns[self.__current_turn]) - 1)


    @property
    def on_last_player(self) -> bool:
        return self.__current_player == (len(self.__players) - 1)


    @property
    def before_first_action(self) -> bool:
        return self.__current_action == -1


    @property
    def on_last_action(self) -> bool:
        return self.__current_action == self.last_action_index


    def add_action(self, action: "GameAction") -> None:
        if not self.in_preset:
            raise IllegalHistoryOperation("Control action invoked in browsing mode!")

        self.__turns[self.__current_turn][self.__current_player].append(action)
        self.__current_action += 1
        self.__log_signal()


    def end_turn(self) -> None:
        if not self.in_preset:
            raise IllegalHistoryOperation("Control action invoked in browsing mode")

        if self.on_last_player:
            self.start_next_game_turn()
        else:
            self.start_next_player_turn()

        Connector().emit('redraw_ui')


    def undo_player_turn(self) -> None:
        if not self.in_preset:
            raise IllegalHistoryOperation("Control action invoked in browsing mode")

        if self.before_first_action:
            if self.at_start:
                return

            self.delete_player_turn()
            if self.on_first_player:
                self.delete_game_turn()

            self.move_to_previous()

        self.undo_player_actions()
        self.clear_player_turn()

        Connector().emit('redraw_ui')


    def move_action_back(self) -> None:
        if not self.before_first_action:
            self.current_action.undo()

        self.move_to_previous()

        Connector().emit('redraw_ui')


    def move_action_forth(self) -> None:
        self.move_to_next()
        if not self.before_first_action:
            self.current_action.execute()

        Connector().emit('redraw_ui')


    def move_turn_back(self) -> None:
        if self.before_first_action:
            if self.at_start:
                return
            self.move_to_previous()
        self.undo_player_actions()
        # Connector().emit('redraw_ui')
        # Connector().emit('redraw_map')


    def move_turn_forth(self) -> None:
        if self.on_last_action:
            if self.in_preset:
                return
            self.move_to_next()

        self.redo_player_actions()

        self.move_to_next()

        # Connector().emit('redraw_ui')
        # Connector().emit('redraw_map')


    def move_to_present(self) -> None:
        while not self.in_preset:
            self.move_turn_forth()


    @property
    def active_player(self) -> IPlayer:
        return self.__players[self.__current_player]


    @property
    def turns_count(self) -> int:
        return len(self.__turns)


    @property
    def remaining_turn(self) -> int:
        return self.__turn_limit - self.turns_count


    @property
    def in_preset(self) -> bool:
        return self.on_present_turn and self.on_present_player and self.on_last_action


    @property
    def at_start(self) -> bool:
        return self.__current_turn == 0 and self.on_first_player and self.before_first_action


    @property
    def current_player(self) -> int:
        return self.__current_player


    @property
    def current_turn(self) -> int:
        return self.__current_turn


    def is_history_log(self, turn: int, player: int, action: int) -> bool:
        if turn < self.current_turn:
            return True

        if turn == self.current_turn:
            if player < self.current_player:
                return True

            if player == self.current_player:
                if action <= self.__current_action:
                    return True

        return False


    def __str__(self):
        result = '<ul>'
        for turn in range(self.turns_count):
            player_turn = self.__turns[turn]
            for p_turn in range(len(player_turn)):
                actions = player_turn[p_turn]
                for i, action in enumerate(actions):
                    color = 'black' if self.is_history_log(turn, p_turn, i) else 'red'
                    result += '<li style="color: {}">Turn {} - Player {}- {}</li>'.format(color, turn, p_turn, action)
        result += '</ul'

        return result
