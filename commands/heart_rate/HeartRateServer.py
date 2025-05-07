# In a new file: heart_rate_server.py
import socket
import threading
import pickle
import time

# Store player heart rates
player_heart_rates = {}
player_connections = {}
hr_lock = threading.Lock()


def start_hr_server(ip='192.168.1.6', port=8081):  # Use different port than game
    hr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hr_socket.bind((ip, port))
    hr_socket.listen(5)
    print(f"Heart rate server listening on {ip}:{port}")

    while True:
        conn, addr = hr_socket.accept()
        print(f"New heart rate connection from {addr}")
        threading.Thread(target=handle_hr_client, args=(conn, addr), daemon=True).start()


def handle_hr_client(conn, addr):
    player_id = None
    try:
        # First message should be player identification
        data = conn.recv(1024)
        player_id = pickle.loads(data)

        with hr_lock:
            player_connections[player_id] = conn

        conn.send(pickle.dumps("Heart rate connection established"))

        # Handle heart rate updates
        while True:
            data = conn.recv(1024)
            if not data:
                break

            request = pickle.loads(data)
            if hasattr(request, 'get_heart_rate'):
                heart_rate = request.get_heart_rate()
                print(f"Player {player_id} heart rate: {heart_rate} BPM")

                with hr_lock:
                    player_heart_rates[player_id] = heart_rate

                    # Send this heart rate to opponent if they're connected
                    send_heart_rate_to_opponent(player_id, heart_rate)

                conn.send(pickle.dumps("Heart rate updated"))

    except Exception as e:
        print(f"Error in heart rate client handler: {e}")
    finally:
        if player_id and player_id in player_connections:
            with hr_lock:
                del player_connections[player_id]
        conn.close()


def send_heart_rate_to_opponent(player_id, heart_rate):
    # Find opponent connection and send them this heart rate
    for pid, conn in player_connections.items():
        if pid != player_id:  # This is an opponent
            try:
                # Create a heart rate update message
                hr_update = {"player_id": player_id, "heart_rate": heart_rate}
                conn.send(pickle.dumps(hr_update))
            except:
                pass  # Ignore errors, they'll be handled in the main loop


# Start the heart rate server in a separate thread
if __name__ == "__main__":
    threading.Thread(target=start_hr_server, daemon=True).start()
    # You could also start your regular game server here