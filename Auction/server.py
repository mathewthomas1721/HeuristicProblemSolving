import socket
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
        print("RECEIVED BID")
        player_bid['received_time'] = datetime.now()

    except:
        player_bid['timeout'] = True

    return player_bid

def send_update(socket, data):
    socket.sendall(data)

class Server():

    DATA_SIZE = 8192

    def __init__(self, host, port, num_player=2):
        """
        :param host: Server host
        :param port: Server port
        """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

        for idx in range(len(self.player_sockets)):
            if valid_players[idx] is True:
                self.pool.apply_async(send_update, (self.player_sockets[idx], data))

    def receive(self, player):
        """Receive a bid from a specific player"""
        print("RECEIVED BID FROM " + str(player))
        return self.player_sockets[player].recv(self.DATA_SIZE)

    def receive_any(self, remain_times):
        """Receive a bid from any player"""
        bids = []

        for player in range(self.num_player):
            r = self.pool.apply_async(recv_from_client, (self.player_sockets[player], player, remain_times[player]))
            bids.append(r)

        bids = [b.get() for b in bids]
        print("BIDS FOR THIS ROUND RECEIVED FROM ALL PLAYERS")
        print(bids)
        return bids

    def close(self):
        """Close server"""
        self.socket.close()

    def __del__(self):
        self.close()
