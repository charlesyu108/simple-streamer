import ring
import selectors
import socket
import threading
import transport


class StreamClient:
    
    def __init__(self, listening_port: int, **kwargs):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client_socket.bind(("", listening_port))
        client_socket.setblocking(False)

        buffer_size = kwargs.get("buffer_size", 1000)
        buffer = ring.RingBuffer(max_size=buffer_size)

        sel = selectors.DefaultSelector()
        sel.register(client_socket, selectors.EVENT_READ, self._socket_callback)

        self.listening_port = listening_port
        self.client_socket = client_socket
        self.buffer = buffer
        self.active = threading.Event()
        self.selector = sel

    def _socket_callback(self, socket, mask):
        data, addr = self.client_socket.recvfrom(transport.CHUNK_SIZE)
        if data:
            self.buffer.add(data)

    def _select_dispatch(self):
        while self.active.is_set():
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def consume_from_buffer(self):
        while self.active.is_set():
            try:
                data = self.buffer.get()
                print(data)
            except ring.EmptyBufferException:
                pass
    

    def start(self):
        try:
            self.active.set()
            dispatch_thread = threading.Thread(target=self._select_dispatch)
            consume_buffer_thread = threading.Thread(target=self.consume_from_buffer)

            dispatch_thread.start()
            consume_buffer_thread.start()

            consume_buffer_thread.join()
            dispatch_thread.join()

        finally:
            self.active.clear()
            self.client_socket.close()


