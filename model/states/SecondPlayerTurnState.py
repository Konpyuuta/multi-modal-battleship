'''

@author Maurice Amon
'''
from model.GameHandler import GameHandler
from model.states.State import State


class SecondPlayerTurnState(State):

    _game_handler = None

    def __init__(self):
        self._game_handler = GameHandler()


    def handle_action(self, coordinates):
        if not self._game_handler.get_game().has_bomb_been_placed(coordinates[0].coordinates[1]):
            self._game_handler.get_game().execute_move(coordinates[0], coordinates[1])
            self._game_handler.set_current_state(self._game_handler.get_turn_state())

        if self._game_handler.get_game().check_is_game_over():
            self._game_handler.set_current_state(self._game_handler.get_game_over_state())