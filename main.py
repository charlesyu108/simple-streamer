# Sample scratch implementation of an audio-broadcast
import sys
import server
import client
import pyaudio
import wave
import transport
import time
import threading
import ring

class Config:
    format = pyaudio.paInt16
    n_channels = 2
    framerate = 44100
    framesize = 4


class ServerImplementation(server.StreamServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pa = pyaudio.PyAudio()
        self.input_audio_stream = self.pa.open(
            format=Config.format,
            rate=Config.framerate,
            channels=Config.n_channels,
            input=True,
        )

    def broadcast(self):
        with self.server_socket:
            frames_per_packet = transport.CHUNK_SIZE//Config.framesize
            while self.active.is_set():
                data = self.input_audio_stream.read(frames_per_packet)
                self.server_socket.sendto(data, ("<broadcast>", self.serving_port))

class ClientImplementation(client.StreamClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pa = pyaudio.PyAudio()
        self.output_audio_stream = self.pa.open(
            format=Config.format,
            rate=Config.framerate,
            channels=Config.n_channels,
            output=True,
        )

    def consume_from_buffer(self):
        while self.active.is_set():
            try:
                data = self.buffer.get()
                self.output_audio_stream.write(data)
            except ring.EmptyBufferException:
                pass
        self.output_audio_stream.stop_stream()
        self.output_audio_stream.close()
        self.pa.terminate()

def start_server():
    print("Starting server...")
    s = ServerImplementation(8089)
    s.start()

def start_client():
    print("Starting client...")
    c = ClientImplementation(8089, buffer_size=1000)
    c.start()


if __name__ == "__main__":
    run_opt = sys.argv[1]
    if run_opt == "server":
        start_server()
    elif run_opt == "client":
        start_client()
    else:
        raise SystemError("Unknown option passed.")
