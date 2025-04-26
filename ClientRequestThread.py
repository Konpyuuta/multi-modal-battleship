'''

@author Maurice Amon
'''
import json
import threading
from datetime import time

from commands.FetchGameStateCommand import FetchGameStateCommand
from commands.MoveCommand import MoveCommand
from commands.StartGameCommand import StartGameCommand
from commands.requests import MoveRequest
from commands.requests.FetchGameStateRequest import FetchGameStateRequest
from commands.requests.RequestTypes import RequestTypes
from commands.requests.StartGameRequest import StartGameRequest


class ClientRequestThread():

    def handle_client(conn, addr, request):
        print("[thread] starting")

        # get the client's message

        command = None
        req_type = request.get_request_type()
        if req_type == RequestTypes.MOVE_REQUEST:
            command = MoveCommand(request, conn)
        elif req_type == RequestTypes.FETCH_REQUEST:
            command = FetchGameStateCommand(request, conn)

        command.execute()

