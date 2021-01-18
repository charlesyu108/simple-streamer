import socket
import time
import threading
import transport

class StreamServer:
    
    def __init__(self, serving_port: int):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.serving_port = serving_port
        self.server_socket = server_socket
        self.active = threading.Event()


    def broadcast(self):
        with self.server_socket:
            while self.active.is_set():
                msg = f"Hello world, {time.time()}"
                transport.redundant_broadcast(
                    msg.encode("utf-8"),
                    self.server_socket,
                    self.serving_port
                )
                time.sleep(1)

    def start(self):
        try:
            self.active.set()
            broadcasting_thread = threading.Thread(target=self.broadcast)
            broadcasting_thread.start()
            broadcasting_thread.join()
        finally:
            self.active.clear()
