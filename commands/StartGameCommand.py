'''

@author Maurice Amon
'''
from commands.Command import Command
from model.board.BattleshipMatrix import BattleshipMatrix


class StartGameCommand(Command):

    def execute(self):
        first_matrix = BattleshipMatrix()
        second_matrix = BattleshipMatrix()
