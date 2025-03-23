'''

@author Maurice Amon
'''
from commands.Command import Command
from model.Game import Game
from model.GameHandler import GameHandler
from model.Player import Player
from model.board.BattleshipMatrix import BattleshipMatrix


class StartGameCommand(Command):

    _start_request = None

    def __init__(self, request):
        self._start_request = request

    def execute(self):
        first_matrix = BattleshipMatrix()
        second_matrix = BattleshipMatrix()
        player1 = Player("Player 1", True, first_matrix)
        player2 = Player("Player 2", False, second_matrix)
        game = Game(player1, player2)
        game_handler = GameHandler(game)
        game_handler.handle()

