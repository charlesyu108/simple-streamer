import socket
import threading

class StreamServer:
    
    def __init__(self, serving_port: int):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.serving_port = serving_port
        self.server_socket = server_socket


    def broadcast(self):
        pass
    

    def start(self):
        with self.server_socket as s:
            broadcasting_thread = threading.Thread(self.broadcast)
            broadcasting_thread.start()
            broadcasting_thread.join()