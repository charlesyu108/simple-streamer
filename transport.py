import hashlib

CHUNK_SIZE = 1024
PACKET_SEND_ATTEMPTS = 5

def broadcast(data: bytes, socket_, port):
    socket_.sendto(data, ("<broadcast>", port))

def redundant_broadcast(data: bytes, socket_, port, attempts=PACKET_SEND_ATTEMPTS):
    for _ in range(PACKET_SEND_ATTEMPTS):
        broadcast(data, socket_, port)