'''

@author Maurice Amon
'''
import pickle
from commands.Command import Command
from commands.requests.FetchGameStateRequest import FetchGameStateRequest
from commands.responses.GameStateResponse import GameStateResponse
from model.GameHandler import GameHandler
from model.board.BattleshipMatrix import BattleshipMatrix


class FetchGameStateCommand(Command):

    _fetch_request = None

    _conn = None

    def __init__(self, request: FetchGameStateRequest, conn):
        self._fetch_request = request
        self._conn = conn


    def execute(self):
        self.update_client()


    def update_client(self):
        player_grid = None
        opponent_grid = None
        game = GameHandler().get_game()
        is_turn = False
        if self._fetch_request.getPlayerID() == game.is_turn().get_name():
            is_turn = True
        if game.get_player1().get_name() == self._fetch_request.getPlayerID():
            player_grid = game.get_player1_battleship_matrix()
            opponent_grid = game.get_player2_battleship_matrix()
        else:
            player_grid = game.get_player2_battleship_matrix()
            opponent_grid = game.get_player1_battleship_matrix()

        game_state = GameStateResponse(player_grid, opponent_grid, is_turn, game.get_game_state(), self._fetch_request)
        if game.check_is_game_over():
            winner = game.get_winner()
            game_state.set_winner(winner)

        message = pickle.dumps(game_state)
        self._conn.send(message)
        self._conn.close()