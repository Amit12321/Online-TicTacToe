import socket
import struct
from pickle import dumps, loads


class Network:
    def __init__(self, server, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)
            # server sends the player back
            buf = b''
            while len(buf) < 4:
                buf += self.client.recv(4 - len(buf))
            length = struct.unpack('!I', buf)[0]
            sent = loads(self.client.recv(length))
            return sent
        except socket.error as e:
            raise e
            

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            buf = b''
            while len(buf) < 4:
                buf += self.client.recv(4 - len(buf))
            length = struct.unpack('!I', buf)[0]
            sent = loads(self.client.recv(length))
            return sent
        except socket.error as e:
            print(e)

    def close(self):
        self.client.close()
