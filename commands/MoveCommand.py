'''

@author Maurice Amon
'''
from commands.Command import Command
from commands.requests.MoveRequest import MoveRequest
from model.GameHandler import GameHandler


class MoveCommand(Command):

    _move_request = None

    _conn = None

    def __init__(self, _move_request: MoveRequest, conn):
        self._move_request = _move_request
        self._conn = conn


    def execute(self):
        game_handler = GameHandler(None)
        column = self._move_request.getCol()
        row = self._move_request.getRow()
        request_list = (self._move_request.getPlayerID(), column, row)
        game_handler.handle(request_list)


    def update_client(self, game_handler: GameHandler):
        battleship_matrix = BattleshipMatrix()
        battleship_matrix.create_battleships()
        message = pickle.dumps(battleship_matrix)
        self._conn.send(message)
        print("Initialized Battleship matrix has been sent to the client: ")
        battleship_matrix.print_matrix()
        self._conn.close()



