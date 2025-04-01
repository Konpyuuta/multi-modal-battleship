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

    _game = None

    _start_state = None

    _first_player_turn_state = None

    _second_player_turn_state = None

    _game_over_state = None

    _current_state = None


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GameHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._start_state = StartGameState()
        self._turn_state = FirstPlayerTurnState(self)
        self._second_player_turn_state = SecondPlayerTurnState(self)
        self._game_over_state = GameOverState(self)
        self._current_state = self._start_state


    def set_game(self, game):
        self._game = game

    def handle(self, object):
        is_game_over = False
        while not is_game_over:
            self._current_state.handle_action(object)




    def get_game(self):
        return self._game


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
