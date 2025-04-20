'''

@author Maurice Amon
'''
from commands.requests.Request import Request
from commands.requests.RequestTypes import RequestTypes
from model.board.BattleshipMatrix import BattleshipMatrix


class FetchGameStateRequest(Request):

    _playerID = None

    _request_type = None

    def __init__(self, request_type: RequestTypes, playerID):
        super()
        self._playerID = playerID
        self._request_type = RequestTypes.MOVE_REQUEST


    def getPlayerID(self):
        return self._playerID

    def getRequestType(self):
        return self._request_type