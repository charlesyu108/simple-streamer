import socket
import threading

class StreamClient:
    
    def __init__(self, listening_port: int):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.listening_port = listening_port
        self.client_socket = client_socket


    def listen(self):
        pass
    

    def start(self):
        with self.client_socket as s:
            s.bind(("", self.listening_port))
            listening_thread = threading.Thread(target=self.listen)
            listening_thread.start()
            listening_thread.join()