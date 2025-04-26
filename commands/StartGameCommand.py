'''

@author Maurice Amon
'''

import pickle
import time

from commands.Command import Command
from commands.requests.StartGameRequest import StartGameRequest
from commands.responses.GameStateResponse import GameStateResponse
from model.Game import Game
from model.GameHandler import GameHandler
from model.Player import Player
from model.PlayerPool import PlayerPool
from model.board.BattleshipMatrix import BattleshipMatrix
from model.states.StartGameState import StartGameState


class StartGameCommand(Command):

    _start_request = None

    _start_request2 = None

    _conn = None

    _conn2 = None

    _name1 = None

    _name2 = None

    _addr1 = None

    _addr2 = None

    def __init__(self, request: StartGameRequest, request2: StartGameRequest, conn, conn2, name1, name2, addr1, addr2):
        self._start_request = request
        self._start_request2 = request2
        self._conn = conn
        self._conn2 = conn2
        self._name1 = name1
        self._name2 = name2
        self._addr1 = addr1
        self._addr2 = addr2

    def execute(self):
        first_matrix = BattleshipMatrix()
        second_matrix = BattleshipMatrix()
        first_matrix.create_battleships()
        second_matrix.create_battleships()
        counter = 10

        player1 = Player(self._addr1, "80", self._name1, True, first_matrix)
        player2 = Player(self._addr2, "80", self._name2, False, second_matrix)
        player1.set_battleship_matrix(first_matrix)
        player1.set_opponent_battleship_matrix(second_matrix)
        player2.set_battleship_matrix(second_matrix)
        player2.set_opponent_battleship_matrix(first_matrix)
        game = Game(player1, player2)
        game_handler = GameHandler()
        game_handler.set_game(game)
        if type(game_handler.get_current_state()).__name__ == StartGameState.__name__:
            game_handler.handle(None)
        PlayerPool._player_pool.append(self._start_request.get_playerID())
        self.update_clients(player1, player2)

    def update_clients(self, player1, player2):
        first_player_game_state = GameStateResponse(player1.get_battleship_matrix(), player2.get_battleship_matrix(),
                                       player1.get_is_turn(), 0, self._start_request)
        second_player_game_state = GameStateResponse(player2.get_battleship_matrix(), player1.get_battleship_matrix(),
                                       player2.get_is_turn(), 0, self._start_request2)
        message = pickle.dumps(first_player_game_state)
        message2 = pickle.dumps(second_player_game_state)
        self._conn.sendall(message)
        self._conn2.sendall(message2)
        print("Initialized Battleship matrix has been sent to the client: ")
        self._conn.close()
        self._conn2.close()

