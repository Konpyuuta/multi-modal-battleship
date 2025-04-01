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
            command = StartGameCommand(request)
        else:
            command = MoveCommand(request)

        command.execute()
        print("[thread] client:", addr, 'recv:', request.get_message())

        # 
        message = "Bye!"
        message = message.encode()
        conn.send(message)
        print("[thread] client:", addr, 'send:', message)

        conn.close()

        print("[thread] ending")
