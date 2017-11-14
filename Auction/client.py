import json
import socket


class Client():

    DATA_SIZE = 8192

    def __init__(self, name, server_address):
        """
        Defines initial client states
        :param name: Player name
        :param server_address: Tuple of (address, port) for server
        """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(server_address)
        self.__send_json({'name': name})

        init_status = self.receive_init()
        self.artists_types = init_status['artists_types']
        self.required_count = init_status['required_count']
        self.auction_items = init_status['auction_items']
        self.init_wealth = init_status['init_wealth']
        self.player_count = init_status['player_count']

    def close(self):
        self.socket.close()

    def __del__(self):
        self.close()

    def __send_json(self, json_object):
        """Helper method to send an object to the server as JSON"""
        self.socket.sendall(bytes(json.dumps(json_object), 'utf-8'))

    def make_bid(self, bid_item, bid_amount):
        """
        Sends player's bid to server and wait for server's reply on round summary
        :param bid_item:
        :param bid_amount:
        :return: dict of auction round summary
        """
        self.__send_json({'bid_item': bid_item, 'bid_amount': bid_amount})
        #print("BID SENT" + str(bid_item) + " " + str(bid_amount))
    def receive_round(self):
        """
        Receives summary of auction round

        The return value is dict with the following keys:
            'finished': boolean flag whether the game is over or not
            'bid_item': auction item
            'bid_winner': winner of this round's bidding
            'auction_round': round number or auction item index
            'remain_players': number of remaining players
        """

        return json.loads(self.socket.recv(self.DATA_SIZE).decode('utf-8'))

    def receive_init(self):
        """
        Receives initial game state

        The return value is a dict with the following keys:
            'artists_types': number of artists
            'required_count': number of items for artist to win
            'auction_items': list of auction items
            'init_wealth': initial wealth per player
            'player_count': number of players in the auction
        """

        return json.loads(self.socket.recv(self.DATA_SIZE).decode('utf-8'))
