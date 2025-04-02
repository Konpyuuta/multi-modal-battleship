'''

@author Maurice Amon
'''
import json
import threading
from datetime import time

from commands.MoveCommand import MoveCommand
from commands.StartGameCommand import StartGameCommand
from commands.requests.RequestTypes import RequestTypes
from commands.requests.StartGameRequest import StartGameRequest


class ClientRequestThread():

    def handle_client(conn, addr, request):
        print("[thread] starting")

        # get the client's message

        command = None
        if type(request).__name__ == StartGameRequest.__name__:
            command = StartGameCommand(request, conn)
        else:
            command = MoveCommand(request, conn)

        command.execute()

