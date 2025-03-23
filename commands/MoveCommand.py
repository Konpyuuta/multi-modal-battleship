'''

@author Maurice Amon
'''
from commands.Command import Command
from commands.requests.MoveRequest import MoveRequest
from model.GameHandler import GameHandler


class MoveCommand(Command):

    _move_request = None

    def __init__(self, _move_request: MoveRequest):
        self._move_request = _move_request


    def execute(self):
        game_handler = GameHandler(None)
        column = self._move_request.getCol()
        row = self._move_request.getRow()
        coordinates = (column, row)
        game_handler.handle(coordinates)



