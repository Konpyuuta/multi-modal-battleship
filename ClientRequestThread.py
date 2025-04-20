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
        if type(request).__name__ == StartGameRequest.__name__:
            command = StartGameCommand(request, conn)
        elif type(request).__name__ == MoveRequest.__name__:
            command = MoveCommand(request, conn)
        elif type(request).__name__ == FetchGameStateRequest.__name__:
            command = FetchGameStateCommand(request, conn)

        command.execute()

