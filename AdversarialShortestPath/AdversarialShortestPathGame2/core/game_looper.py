from __future__ import print_function

from connector.server import Server
from core.game_state import Game


class GameLooper(object):
    def __init__(self, address, port, game_file):
        self.game = Game(game_file)
        print('Game Loaded...')
        self.server = Server(address, port)
        print("Server started on port {}...".format(port))

    def run_game_loop(self):
        print("Waiting for players to connect...")
        player_info = self.server.connect_players()

        self.game.set_players(player_info)
        print("Players connected, sending game!")
        self.server.send_update(self.game.full_state())

        self.game.start_game()
        print("Game Started!")

        while not self.game.done():
            move = self.server.receive(self.game.chance)
            update, status = self.game.make_move(move)
            self.server.send_update(update)
            print(status + '\n')
