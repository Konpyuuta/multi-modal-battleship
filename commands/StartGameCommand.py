'''

@author Maurice Amon
'''

import pickle

import main
from commands.Command import Command
from commands.requests.StartGameRequest import StartGameRequest
from model.Game import Game
from model.GameHandler import GameHandler
from model.Player import Player
from model.board.BattleshipMatrix import BattleshipMatrix


class StartGameCommand(Command):

    _start_request = None

    _conn = None

    def __init__(self, request: StartGameRequest, conn):
        self._start_request = request
        self._conn = conn

    def execute(self):
        first_matrix = BattleshipMatrix()
        second_matrix = BattleshipMatrix()
        player1 = Player("Player 1", True, first_matrix)
        player2 = Player("Player 2", False, second_matrix)
        main.player_list.append(self._start_request.get_playerID())
        self.update_client()
        game = Game(player1, player2)
        game_handler = GameHandler()
        #game_handler.handle()

    def update_client(self):
        battleship_matrix = BattleshipMatrix()
        battleship_matrix.create_battleships()
        message = pickle.dumps(battleship_matrix)
        self._conn.send(message)
        print("Initialized Battleship matrix has been sent to the client: ")
        battleship_matrix.print_matrix()
        self._conn.close()

