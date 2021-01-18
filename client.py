import ring
import socket
import time
import threading
import transport


class StreamClient:
    
    def __init__(self, listening_port: int):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.listening_port = listening_port
        self.client_socket = client_socket
        self.buffer = ring.DedupeRingBuffer()
        self.active = threading.Event()

    def listen(self):
        with self.client_socket:
            self.client_socket.bind(("", self.listening_port))
            while self.active.is_set():
                data, addr = self.client_socket.recvfrom(transport.CHUNK_SIZE)
                if data:
                    self.buffer.add(data)
                time.sleep(1)

    def play(self):
        while self.active.is_set():
            try:
                data = self.buffer.get()
                print(data)
            except ring.EmptyBufferException:
                pass
            time.sleep(1)
    

    def start(self):
        try:
            listening_thread = threading.Thread(target=self.listen)
            playing_thread = threading.Thread(target=self.play)

            self.active.set()
        
            listening_thread.start()
            playing_thread.start()

            playing_thread.join()
            listening_thread.join()
        finally:
            self.active.clear()

