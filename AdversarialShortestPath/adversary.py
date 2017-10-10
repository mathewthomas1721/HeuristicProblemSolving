from __future__ import print_function

import random
import math
import argparse
import asp
import dijkstra
from client import Client


'''def get_args():
    parser = argparse.ArgumentParser("Adversarial Client for the game")
    parser.add_argument('--ip', default='127.0.0.1',
                        help='IP address of the game server')
    parser.add_argument('--port', default=8080, type=int,
                        help='Port of the game server')
    parser.add_argument('--name', default='BabySnakes',
                        help='Name of the bot')
    return parser.parse_args()'''


'''def next_edge_to_increase_cost():
    """
    Add Agent logic here
    """
    first_node = random.choice(game['graph'].keys())
    second_node = random.choice(game['graph'][first_node])
    return first_node, second_node'''


if __name__ == "__main__":
    args = get_args()
    client = Client(sys.argv[1], int(sys.argv[2]), sys.argv[3], 1)
    game = client.get_game()
    start,end,graphMat = asp.populateGraph(game)
    Dpaths = dijkstra.dijkstra(graphMat,end)

    players_move = client.receive_data()
    print("Player currently at " + str(players_move['position']))
    done = players_move['done']

    start = int(players_move['position'])


    while not done:
        node1, node2 = asp.get_A_move(Dpaths, graphMat, start, end)
        update = client.send_cost_update(str(node1), str(node2))
        print("Edge affected = " + str(update['edge']) + " to " + str(update['new_cost']))
        if update['done']:
            break
        players_move = client.receive_data()
        print("Player currently at " + str(players_move['position']))
        done = players_move['done']
        start = int(players_move['position'])
