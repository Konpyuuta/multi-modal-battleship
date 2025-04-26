'''

@author Maurice Amon
'''
import pickle

from commands.Command import Command
from commands.requests.MoveRequest import MoveRequest
from commands.responses.GameStateResponse import GameStateResponse
from model.GameHandler import GameHandler


class MoveCommand(Command):

    _move_request = None

    _conn = None

    def __init__(self, _move_request: MoveRequest, conn):
        self._move_request = _move_request
        self._conn = conn


    def execute(self):
        game_handler = GameHandler()
        column = self._move_request.getCol()
        row = self._move_request.getRow()
        request_list = [self._move_request.getPlayerID(), column, row]
        game_handler.handle(request_list)
        game = game_handler.get_game()
        is_turn = False
        if self._move_request.getPlayerID() == game.is_turn().get_name():
            is_turn = True
        b1 = game_handler.get_game().get_player1_battleship_matrix()
        b2 = game_handler.get_game().get_player2_battleship_matrix()
        game_state = GameStateResponse(b1, b2, is_turn, None, self._move_request)
        message = pickle.dumps(game_state)
        self._conn.send(message)
        self._conn.close()





