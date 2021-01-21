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
    n_channels = 1
    framerate = 4000 # Reduced this from 41000
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
            stream_callback=self.callback,
            frames_per_buffer=transport.CHUNK_SIZE//Config.framesize
        )

    def consume_from_buffer(self):
        self.output_audio_stream.start_stream()
        while self.active.is_set() and self.output_audio_stream.is_active():
            time.sleep(5)
        self.output_audio_stream.stop_stream()
        self.output_audio_stream.close()
        self.pa.terminate()

    def callback(self, in_data, frame_count, time_info, status):
        frames_per_packet = transport.CHUNK_SIZE//Config.framesize
        data_out = b""
        frames_read = 0
        while frames_read < frames_per_packet:
            try:
                data = self.buffer.get()
                data_out += data
                frames_read += frames_per_packet
            except ring.EmptyBufferException:
                continue
        return (data_out, pyaudio.paContinue)

def start_server():
    print("Starting server...")
    s = ServerImplementation(8089)
    s.start()

def start_client():
    print("Starting client...")
    c = ClientImplementation(8089)
    c.start()


if __name__ == "__main__":
    run_opt = sys.argv[1]
    if run_opt == "server":
        start_server()
    elif run_opt == "client":
        start_client()
    else:
        raise SystemError("Unknown option passed.")
