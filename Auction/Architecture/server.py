import socket as sck
import json
from datetime import datetime
from multiprocessing import Pool


def recv_from_client(socket, player, remain_time):

    player_bid = dict()
    player_bid['player'] = player
    player_bid['start_time'] = datetime.now()
    player_bid['timeout'] = False

    try:
        socket.settimeout(remain_time)
        data = socket.recv(Server.DATA_SIZE).decode('utf-8')

        player_bid['bid'] = json.loads(data)
        player_bid['received_time'] = datetime.now()

    except sck.timeout:
        player_bid['timeout'] = True

    return player_bid

def send_update(socket, data):
    socket.setblocking(True)
    socket.sendall(data)
    return True

class Server():

    DATA_SIZE = 8192

    def __init__(self, host, port, num_player=2):
        """
        :param host: Server host
        :param port: Server port
        """

        self.socket = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
        self.socket.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.player_sockets = [None] * num_player
        self.socket.listen(num_player)

        self.num_player = len(self.player_sockets)
        self.pool = Pool(processes=self.num_player)

    def establish_connection(self):
        """Establishes connection with players"""
        for i in range(self.num_player):
            self.player_sockets[i], _ = self.socket.accept()
        res = map(self.receive, range(self.num_player))
        return res

    def update_all_clients(self, data, valid_players):
        """Updates all players by sending data to client sockets"""
        results = []
        for idx in range(len(self.player_sockets)):
            if valid_players[idx] is True:
                results.append(self.pool.apply_async(send_update, (self.player_sockets[idx], data)))
        return [r.get() for r in results]

    def receive(self, player):
        """Receive a bid from a specific player"""
        return self.player_sockets[player].recv(self.DATA_SIZE)

    def receive_any(self, remain_times):
        """Receive a bid from any player"""
        bids = []

        for player in range(self.num_player):
            r = self.pool.apply_async(recv_from_client, (self.player_sockets[player], player, remain_times[player]))
            bids.append(r)

        bids = [b.get() for b in bids]

        return bids

    def close(self):
        """Close server"""
        self.socket.close()

    def __del__(self):
        self.close()
