'''

@author Maurice Amon
'''
import threading
from datetime import time


class ClientRequestThread():

    def handle_client(conn, addr):
        print("[thread] starting")

        # get the client's message
        message = conn.recv(2048)
        message = message.decode()
        print("[thread] client:", addr, 'recv:', message)

        # 
        message = "Bye!"
        message = message.encode()
        conn.send(message)
        print("[thread] client:", addr, 'send:', message)

        conn.close()

        print("[thread] ending")
