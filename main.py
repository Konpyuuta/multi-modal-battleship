'''

@author Maurice Amon
@description Main-file for handling all the incoming requests ..
'''
import json
import pickle
import threading
from asyncio import wait
import time
import socket

from ClientRequestThread import ClientRequestThread
from commands.StartGameCommand import StartGameCommand
from commands.requests.Request import Request
from commands.requests.StartGameRequest import StartGameRequest
from model.Player import Player
from model.board.BattleshipMatrix import BattleshipMatrix
#data = Player()
#data.set_name("Mauzi")
#data_string = pickle.dumps(data)
#print ('PICKLE:', pickle.loads(data_string).get_name())
#ba = BattleshipMatrix()
#ba.create_battleships()
#ba.print_matrix()
# All parallel threads ..
thread_pool = []

# constants for the server ...

ip = '127.0.0.1'
port = 8080

is_started = False
clients = []
lock = threading.Lock()
game_not_started = True


# start the server ...
#s = socket.socket()
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s.bind((ip, port))
#s.listen(1)


def wait(conn, addr, request):
    global game_not_started
    global is_started
    with lock:
        clients.append((conn, addr, request))

    while True:
        with lock:
            print("Wait for the second Player")
            if len(clients) == 2:
                game_not_started = False
                break
    if not is_started:
        start_command = StartGameCommand(clients[0][2], clients[1][2], clients[0][0], clients[1][0], clients[0][2].get_playerID(), clients[1][2].get_playerID(), clients[0][1], clients[1][1])
        start_command.execute()
        is_started = True

def process_client_requests(conn, addr):
    try:
        client_msg = conn.recv(2048)
        request = pickle.loads(client_msg)
        if not game_not_started:
            t = threading.Thread(target=ClientRequestThread.handle_client, args=(conn, addr, request), daemon=True)
            t.start()
            thread_pool.append(t)
        else:
            threading.Thread(target=wait, args=(conn, addr, request), daemon=True).start()
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        for t in thread_pool:
            t.join()

def start_server():
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((ip, port))
    # Server is ready for client requests..
    socket_server.listen()
    while True:
        conn, addr = socket_server.accept()
        # Process the request ..
        process_client_requests(conn, addr)
    # end while
# end function


if __name__ == '__main__':
    start_server()



