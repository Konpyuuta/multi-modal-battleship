'''

@author Maurice Amon
'''
import pickle
from commands.Command import Command
from commands.requests.FetchGameStateRequest import FetchGameStateRequest
from commands.responses.GameStateResponse import GameStateResponse
from model.board.BattleshipMatrix import BattleshipMatrix


class FetchGameStateCommand(Command):

    _fetch_request = None

    _conn = None

    def __init__(self, request: FetchGameStateRequest, conn):
        print("Heeeeloooooooo")
        self._fetch_request = request
        self._conn = conn


    def execute(self):
        self.update_client()


    def update_client(self):
        battleship_matrix = BattleshipMatrix()
        battleship_matrix.create_battleships()
        battleship_matrix2 = BattleshipMatrix()
        battleship_matrix2.create_battleships()
        game_state = GameStateResponse(battleship_matrix, battleship_matrix2, 0, self._fetch_request)

        message = pickle.dumps(game_state)
        self._conn.send(message)
        print("Updated Battleship matrix has been sent to the client: ")
        battleship_matrix.print_matrix()
        self._conn.close()