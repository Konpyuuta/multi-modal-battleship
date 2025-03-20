'''

@author Maurice Amon

@description In charge of implementing the game logic of our Enhanced Battleship.
             Uses a deterministic finite Automaton (DFA) to implement the rules.
             Takes an input from the socket-stream to trigger the rule-enforcement.
'''
from model.logic.states.GameOverState import GameOverState
from model.logic.states.StartGameState import StartGameState
from model.states.FirstPlayerTurnState import FirstPlayerTurnState
from model.states.SecondPlayerTurnState import SecondPlayerTurnState


class GameHandler:

    _start_state = None

    _first_player_turn_state = None

    _second_player_turn_state = None

    _game_over_state = None

    _current_state = None

    def __init__(self, game):
        self._start_state = StartGameState(game)
        self._turn_state = FirstPlayerTurnState(game)
        self._second_player_turn_state = SecondPlayerTurnState(game)
        self._game_over_state = GameOverState(game)
        self._current_state = self._start_state


    def handle(self):
        is_game_over = False
        while not is_game_over:
            self._current_state.handle_action()


    def set_current_state(self, state):
        self._current_state = state


    def get_current_state(self):
        return self._current_state

    def get_game_over_state(self):
        return self._game_over_state

    def get_start_state(self):
        return self._start_state

    def get_turn_state(self):
        return self._turn_state

    def get_second_player_turn_state(self):
        return self._second_player_turn_state
