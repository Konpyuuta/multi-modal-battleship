'''

@author Maurice Amon
'''
from model.states.State import State


class StartGameState(State):

    _game_handler = None

    def __init__(self, game_handler):
        self._game_handler = game_handler

    def handle_action(self, object):
        # Initialize the game
        self._game_handler.set_current_state(self._game_handler.get_turn_state())
