import socket
import json


class Server(object):
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.sockets = [None, None]
        self.socket.listen(2)

    def connect_players(self):
        self.sockets[0], _ = self.socket.accept()
        self.sockets[1], _ = self.socket.accept()
        return [self.receive(0), self.receive(1)]

    def send_update(self, data):
        for sck in self.sockets:
            sck.sendall(json.dumps(data))

    @staticmethod
    def byteify(input):
        if isinstance(input, dict):
            return {Server.byteify(key): Server.byteify(value)
                    for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [Server.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    def receive(self, which):
        return Server.byteify(json.loads(self.sockets[which].recv(1024)))

    def close(self):
        self.socket.close()

    def __del__(self):
        self.close()
