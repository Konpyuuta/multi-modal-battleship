'''

@author Maurice Amon
@description Main-file for handling all the incoming requests ..
'''
import pickle
import threading
from socket import socket

import ClientRequestThread
from model.Player import Player
from model.board.BattleshipMatrix import BattleshipMatrix
data = Player()
data.set_name("Mauzi")
data_string = pickle.dumps(data)
print ('PICKLE:', pickle.loads(data_string).get_name())
ba = BattleshipMatrix()
ba.create_battleships()
ba.print_matrix()
# All parallel threads ..
thread_pool = []

# constants for the server ...

ip = '127.0.0.1'
port = 50052


# start the server ...
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((ip, port))
s.listen(1)


def process_client_requests():
    try:
        while True:
            print("Waiting for client")
            conn, addr = s.accept()

            print("Client:", addr)

            t = threading.Thread(target=ClientRequestThread.ClientRequestThread.handle_client, args=(conn, addr))
            t.start()

            thread_pool.append(t)
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        if s:
            s.close()
        for t in thread_pool:
            t.join()