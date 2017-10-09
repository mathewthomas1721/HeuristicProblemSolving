from __future__ import print_function

from enum import Enum
import time


class Gamer(object):
    class Type(Enum):
        PLAYER = 1
        ADVERSARY = 2

        @classmethod
        def tostring(cls, val):
            for k, v in vars(cls).iteritems():
                if v == val:
                    return k

    def __init__(self, gamer_type, total_moves):
        self.moves = []
        self.type = gamer_type
        self.name = Gamer.Type.tostring(self.type)
        self.player_time = None
        self.time_available = 120
        self.player_cost = 0
        self.moves_made = 0
        self.total_moves = total_moves

    def get_last_move(self):
        return self.moves[-1]

    def reset_timer(self):
        self.player_time = time.time()

    def time_left(self):
        self.time_available -= time.time() - self.player_time
        self.player_time = None
        return self.time_available

    def switch_player(self):
        pass

    def set_name(self, name):
        self.name = name
        print("Added {}: {}".format(Gamer.Type.tostring(self.type), self.name))

    def moves_left(self):
        total_moves_left = self.total_moves - self.moves_made
        return total_moves_left > 0

    def make_move(self, graph_map, move):
        if self.time_left() < 0:
            cost, edge, done, error = 0, 0, True, True
            print("Player {} ran out of time.".format(self.name))
            return edge, cost, done, error, self.time_available

        if not self.moves_left():
            cost, edge, done, error = 0, 0, True, True
            print("Player {} ran out of moves.".format(self.name))
            return edge, cost, done, error, self.time_available

        if self.type == Gamer.Type.PLAYER:
            edge = move['start_node'], move['end_node']
            cost, done = graph_map.move_edge(edge)
            error = False
            self.player_cost += cost
        else:
            edge = move['node_1'], move['node_2']
            cost = graph_map.update_edge(edge)
            done, error = False, False

        self.moves_made += 1

        return edge, cost, done, error, self.time_available

