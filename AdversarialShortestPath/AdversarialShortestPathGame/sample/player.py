from __future__ import print_function

import argparse
import random
import asp
import dijkstra
from client import Client


def get_args():
    parser = argparse.ArgumentParser("Adversarial Client for the game")
    parser.add_argument('--ip', default='127.0.0.1',
                        help='IP address of the game server')
    parser.add_argument('--port', default=8080, type=int,
                        help='Port of the game server')
    parser.add_argument('--name', default='Player',
                        help='Name of the bot')
    return parser.parse_args()


'''def next_edge_to_move():
   
    return first_node, second_node'''


if __name__ == "__main__":
    args = get_args()
    client = Client(args.ip, args.port, args.name, 0)
    game = client.get_game()
    start,end,graphMat = asp.populateGraph(game)
    Dpaths = dijkstra.dijkstra(graphMat,end)
    while True:
        node1, node2 = asp.get_move(Dpaths, graphMat, start, end)
        update = client.send_edge_move(str(node1), str(node2))
        print ("Moved to " + str(update['position']))
        if update['done']:
            break
        
        adversaries_move = client.receive_data()
        print("Edge affected = " + str(adversaries_move['edge']) + " to " + str(adversaries_move['new_cost']))
        if adversaries_move['done']:
            break
        start = int(node2)    
        asp.updateGraph(int(adversaries_move['edge'][0]), int(adversaries_move['edge'][0]), int(adversaries_move['new_cost']))