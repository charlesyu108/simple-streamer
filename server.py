import socket
import time
import threading

class StreamServer:
    
    def __init__(self, serving_port: int):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.serving_port = serving_port
        self.server_socket = server_socket


    def broadcast(self):
        while True:
            self.server_socket.sendto(b"Hello world", ("<broadcast>", self.serving_port))
            time.sleep(1)
    

    def start(self):
        with self.server_socket as s:
            broadcasting_thread = threading.Thread(target=self.broadcast)
            broadcasting_thread.start()
            broadcasting_thread.join()
