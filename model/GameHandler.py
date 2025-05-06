'''

@author Maurice Amon

@description In charge of implementing the game logic of our Enhanced Battleship.
             Uses a deterministic finite Automaton (DFA) to implement the rules.
             Takes an input from the socket-stream to trigger the rule-enforcement.
'''
from Singleton import Singleton
from model.states.FirstPlayerTurnState import FirstPlayerTurnState
from model.states.GameOverState import GameOverState
from model.states.SecondPlayerTurnState import SecondPlayerTurnState
from model.states.StartGameState import StartGameState
from observer.Observable import Observable
from observer.Observer import Observer
from commands.requests.RequestTypes import RequestTypes


class GameHandler(metaclass=Singleton):

    _game = None

    _start_state = None

    _first_player_turn_state = None

    _second_player_turn_state = None

    _game_over_state = None

    _current_state = None

    _state_description = None

    _initialized = False

    _heart_rate_handler = None


    def __init__(self):
        if not self._initialized:
            self._start_state = StartGameState(self)
            self._turn_state = FirstPlayerTurnState(self)
            self._second_player_turn_state = SecondPlayerTurnState(self)
            self._game_over_state = GameOverState(self)
            self._current_state = self._start_state
            self._initialized = True

            from model.HeartRateHandler import HeartRateHandler
            self._heart_rate_handler = HeartRateHandler(self)


    def set_game(self, game):
        self._game = game

    def handle(self, object):
        print("Execute Action")
        print(self._current_state)
        self._current_state.handle_action(object)

    def handle_request(self, request, player_id):
        request_type = request.get_type()
        # Heart rate requests don't affect game state
        if request_type == RequestTypes.HEART_RATE:
            return self._heart_rate_handler.handle(request, player_id)
        else:
            # For regular game actions, use the state machine
            self.handle(request)

            # Return a response based on the current state
            # You'll need to implement appropriate Response classes
            from model.responses.Response import Response
            return Response(request_type, True, self._state_description)


    def get_latest_state_description(self):
        return self._state_description

    def set_latest_state_description(self, state_description):
        self._state_description = state_description

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

