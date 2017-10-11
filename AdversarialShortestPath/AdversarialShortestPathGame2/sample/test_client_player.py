from __future__ import print_function

import argparse
import random

from connector.client import Client


def get_args():
    parser = argparse.ArgumentParser("Adversarial Client for the game")
    parser.add_argument('--ip', default='127.0.0.1',
                        help='IP address of the game server')
    parser.add_argument('--port', default=8080, type=int,
                        help='Port of the game server')
    parser.add_argument('--name', default='Player',
                        help='Name of the bot')
    return parser.parse_args()


def next_edge_to_move():
    """
    Add Agent logic here
    """
    first_node = random.choice(game['graph'].keys())
    second_node = random.choice(game['graph'][first_node])
    return first_node, second_node


if __name__ == "__main__":
    args = get_args()
    client = Client(args.ip, args.port, args.name, 0)
    game = client.get_game()

    while True:
        start, end = next_edge_to_move()
        update = client.send_edge_move(start, end)
        print(update)
        if update['done']:
            break

        adversaries_move = client.receive_data()
        print(adversaries_move)
        if adversaries_move['done']:
            break
