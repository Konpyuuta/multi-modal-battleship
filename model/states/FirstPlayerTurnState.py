'''

@author Maurice Amon
'''
from model.PlayerPool import PlayerPool
from model.states.State import State


class FirstPlayerTurnState(State):

    _game_handler = None

    def __init__(self, game_handler):
        self._game_handler = game_handler


    def handle_action(self, coordinates):
        print(f"ID: {coordinates[0]}")
        print(f"Current Player: {self._game_handler.get_game().get_player1().get_name()}")
        if not coordinates[0] == self._game_handler.get_game().get_player1().get_name():
            self._game_handler.set_latest_state_description("It's not your turn!")
            return False


        if not self._game_handler.get_game().get_player2_battleship_matrix().has_bomb_been_placed(coordinates[1], coordinates[2]):
            self._game_handler.get_game().execute_move(coordinates[1], coordinates[2])
            self._game_handler.set_current_state(self._game_handler.get_second_player_turn_state())
            self._game_handler.set_latest_state_description("Move was successfully executed! ")
        else:
            self._game_handler.set_latest_state_description("A bomb has already been placed on this field!.")


        if self._game_handler.get_game().check_is_game_over():
            self._game_handler.set_current_state(self._game_handler.get_game_over_state())

    def is_player_turn(self, player_id):
        if PlayerPool._player_pool[0] == player_id:
            return True
        return False