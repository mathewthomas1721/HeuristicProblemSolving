import atexit

from client import Client
import time
import random
import sys

def check_game_status(state):

    if state['bid_winner'] is not None:
        print('Player {} won {} on this round {} with bid amount {}.'
              .format(state['bid_winner'], state['bid_item'], state['auction_round'], state['winning_bid']))
    else:
        print('No bidders in this round {}.'.format(state['auction_round']))

    print('-------------------------------')

    if state['finished']:
        print('Game over\n{}\n'.format(state['reason']))
        exit(0)

def calculate_bid(game_state, wealth):

    """Insert algorithm here"""
    return random.randrange(0, wealth)

if __name__ == '__main__':

    ip = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3] if len(sys.argv) == 4 else 'player_1'

    client = Client(name, (ip, port))
    atexit.register(client.close)

    artists_types = client.artists_types
    required_count = client.required_count
    auction_items = client.auction_items
    wealth = client.init_wealth

    current_round = 0

    while True:
        bid_amt = calculate_bid(None, wealth)
        client.make_bid(auction_items[current_round], bid_amt)

        # after sending bid, wait for other player
        game_state = client.receive_round()
        if game_state['bid_winner'] == name:
            wealth -= game_state['winning_bid']
        check_game_status(game_state)

        current_round += 1