'''

@author Maurice Amon
'''
import json
import threading
from datetime import time

from commands.MoveCommand import MoveCommand
from commands.StartGameCommand import StartGameCommand
from commands.requests.RequestTypes import RequestTypes


class ClientRequestThread():

    def handle_client(conn, addr):
        print("[thread] starting")

        # get the client's message
        message = conn.recv(2048)
        message = message.decode()
        request = json.loads(message)
        command = None
        if request.get_request_type() == RequestTypes.move_request_type:
            command = MoveCommand(request)

        else:
            command = StartGameCommand(request)

        command.execute()
        print("[thread] client:", addr, 'recv:', message)

        # 
        message = "Bye!"
        message = message.encode()
        conn.send(message)
        print("[thread] client:", addr, 'send:', message)

        conn.close()

        print("[thread] ending")
