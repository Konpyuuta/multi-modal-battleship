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
from commands.requests.RequestTypes import RequestTypes
from commands.requests.Request import Request
from commands.requests.StartGameRequest import StartGameRequest
from model.Player import Player
from model.board.BattleshipMatrix import BattleshipMatrix
from commands.heart_rate.HeartRateServer import HeartRateServer

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

ip = '192.168.1.6'
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

        if hasattr(request, 'get_request_type') and request.get_request_type() == RequestTypes.HEART_RATE:
            t = threading.Thread(target=ClientRequestThread.handle_client, args=(conn, addr, request), daemon=True)
            t.start()
            thread_pool.append(t)
        elif not game_not_started:
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
    try:
        print(f"Creating game server socket on {ip}:{port}")
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            print(f"Binding game server to {ip}:{port}")
            socket_server.bind((ip, port))
            print(f"Successfully bound to {ip}:{port}")
        except Exception as e:
            print(f"ERROR BINDING GAME SERVER: {e}")
            return

        # Server is ready for client requests
        print(f"Game server listening on {ip}:{port}")
        socket_server.listen()

        print("Entering main connection acceptance loop")
        while True:
            print("Waiting for client connection...")
            conn, addr = socket_server.accept()
            print(f"Game server received connection from {addr}")
            # Process the request
            process_client_requests(conn, addr)

    except Exception as e:
        print(f"CRITICAL ERROR IN GAME SERVER: {e}")
        import traceback
        traceback.print_exc()


# In your server-side main.py
if __name__ == '__main__':
    print("Starting Battleship game servers...")

    # Start heart rate server in a dedicated thread
    hr_thread = threading.Thread(target=lambda: HeartRateServer(ip).start(), daemon=True)
    hr_thread.start()
    print("Heart rate server started in background thread")

    # Give it a moment to initialize
    time.sleep(1)

    # Start the main game server in its own dedicated thread
    game_thread = threading.Thread(target=start_server, daemon=True)
    game_thread.start()
    print("Game server started in background thread")

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down servers...")



