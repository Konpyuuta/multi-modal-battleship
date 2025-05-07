# In a new file: heart_rate_server.py
import socket
import threading
import pickle
import time


class HeartRateServer:
    """Class to handle heart rate server functionality"""

    def __init__(self, ip, port=8081):
        self.ip = ip
        self.port = port
        self.player_heart_rates = {}
        self.player_hr_connections = {}
        self.hr_lock = threading.Lock()
        self.running = False
        self.hr_thread = None

    def start(self):
        """Start the heart rate server in a background thread"""
        if self.running:
            print("Heart rate server is already running")
            return

        self.running = True
        self.hr_thread = threading.Thread(target=self._run_server, daemon=True)
        self.hr_thread.start()
        print(f"Heart rate server listening on {self.ip}:{self.port}")

    def _run_server(self):
        """Main server function running in a separate thread"""
        try:
            hr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            hr_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            hr_socket.bind((self.ip, self.port))
            hr_socket.listen(5)

            while self.running:
                try:
                    conn, addr = hr_socket.accept()
                    print(f"New heart rate connection from {addr}")
                    threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True).start()
                except Exception as e:
                    print(f"Error accepting HR connection: {e}")
        except Exception as e:
            print(f"Heart rate server error: {e}")
        finally:
            print("Heart rate server stopped")

    def _handle_client(self, conn, addr):
        """Handle a client connection for heart rate updates"""
        player_id = None
        try:
            # First message should be player identification
            data = conn.recv(1024)
            player_id = pickle.loads(data)
            print(f"Player {player_id} connected for heart rate updates")

            with self.hr_lock:
                self.player_hr_connections[player_id] = conn

            conn.send(pickle.dumps("Heart rate connection established"))

            # Handle heart rate updates
            while self.running:
                data = conn.recv(1024)
                if not data:
                    break

                request = pickle.loads(data)
                if hasattr(request, 'get_heart_rate'):
                    heart_rate = request.get_heart_rate()
                    print(f"Player {player_id} heart rate: {heart_rate} BPM")

                    with self.hr_lock:
                        self.player_heart_rates[player_id] = heart_rate

                        # Send this heart rate to opponent if they're connected
                        for pid, connection in self.player_hr_connections.items():
                            if pid != player_id:  # This is an opponent
                                try:
                                    # Create a heart rate update message
                                    connection.send(pickle.dumps({"player_id": player_id, "heart_rate": heart_rate}))
                                except Exception as e:
                                    print(f"Error sending HR to opponent {pid}: {e}")

                    conn.send(pickle.dumps("Heart rate updated"))

        except Exception as e:
            print(f"Error in heart rate client handler: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print(f"Heart rate connection for player {player_id} closed")
            if player_id and player_id in self.player_hr_connections:
                with self.hr_lock:
                    del self.player_hr_connections[player_id]
            try:
                conn.close()
            except:
                pass

    def stop(self):
        """Stop the heart rate server"""
        self.running = False
        # Close all connections
        with self.hr_lock:
            for player_id, conn in self.player_hr_connections.items():
                try:
                    conn.close()
                except:
                    pass
            self.player_hr_connections.clear()
            self.player_heart_rates.clear()

        print("Heart rate server stopped")