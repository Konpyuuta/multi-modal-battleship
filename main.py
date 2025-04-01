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


# start the server ...
#s = socket.socket()
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s.bind((ip, port))
#s.listen(1)


def process_client_requests(conn, addr):
    try:
        while True:
            print("Client:", addr)
            client_msg = conn.recv(2048)
            request = pickle.loads(client_msg)
            print(type(request).__name__)
            print(StartGameRequest.__name__)
            if type(request).__name__ == StartGameRequest.__name__:
                print("It is a valid request!")
            t = threading.Thread(target=ClientRequestThread.handle_client, args=(conn, addr, request), daemon=True)
            t.start()
            thread_pool.append(t)
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    finally:
        '''if s:
            s.close()
        for t in thread_pool:
            t.join()'''

def start_server():
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((ip, port))

    # Server is ready for client requests..
    socket_server.listen()

    conn, addr = socket_server.accept()
    print('New client got connected ..')
    # Process the request ..
    process_client_requests(conn, addr)
    myCounter = 0
    while True:
        message = 'message ' + str(myCounter)
        print('sending: ' + message)
        sendTextViaSocket(message, conn)
        myCounter += 1
        time.sleep(1)
    # end while
# end function

def sendTextViaSocket(message, sock):
    # encode the text message
    encodedMessage = bytes(message, 'utf-8')

    # send the data via the socket to the server
    sock.sendall(encodedMessage)

    # receive acknowledgment from the server
    encodedAckText = sock.recv(1024)
    ackText = encodedAckText.decode('utf-8')

    # log if acknowledgment was successful
    if ackText == "ACK_TEXT":
        print('server acknowledged reception of text')
    else:
        print('error: server has sent back ' + ackText)
    # end if
# end function

if __name__ == '__main__':
    start_server()



