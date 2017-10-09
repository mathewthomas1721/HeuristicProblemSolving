from __future__ import print_function

from core.player import Gamer
from core.graph import GraphMapState


class Game(object):
    def __init__(self, game_file):
        self.graph_map = GraphMapState.init_from_textfile(game_file)
        self.player = [Gamer(Gamer.Type.PLAYER, 2*len(self.graph_map.graph.nodes)),
                       Gamer(Gamer.Type.ADVERSARY, 2*len(self.graph_map.graph.nodes))]
        self.chance = 0
        self.game_running = False

    def set_players(self, players_info):
        if players_info[0]['type'] == 1:
            self.player = self.player[::-1]
            self.chance = 1
        self.player[0].set_name(players_info[0]['name'])
        self.player[1].set_name(players_info[1]['name'])

    def done(self):
        return not self.game_running

    def start_game(self):
        self.game_running = True
        self.player[self.chance].reset_timer()

    def end_game(self):
        self.game_running = False

    def make_move(self, move):
        edge, cost, done, error, time_left = self.player[self.chance].make_move(self.graph_map,
                                                                                move)
        if done:
            self.end_game()
        update = self.get_update(edge, cost, done, error)
        self.switch_player()

        return update, self.format_update(update, time_left)

    def get_update(self, edge, cost, done, error):
        update = dict()
        update['edge'] = edge
        if self.player[self.chance].type == Gamer.Type.PLAYER:
            update['add_cost'] = cost
        else:
            update['new_cost'] = cost
        update['done'] = done
        update['error'] = error
        update['position'] = self.graph_map.current_position
        return update

    def format_update(self, update, time_left):
        if update['done']:
            which = 0 if self.player[0].type == Gamer.Type.PLAYER else 1
            return 'Game Done! \n Player has a total cost: {}'.format(
                self.player[which].player_cost)
        if 'add_cost' in update:
            if update['add_cost']:
                ret = 'Player moved from {} to {} adding cost {}'.format(update['edge'][0],
                                                                         update['edge'][1],
                                                                         update['add_cost'])
            else:
                 ret = 'Player made an empty movement for edge {}, {}'.format(update['edge'][0],
                                                                              update['edge'][1])
        else:
            if update['new_cost']:
                ret = 'Adversary made edge {}, {} cost to {}'.format(update['edge'][0],
                                                                     update['edge'][1],
                                                                     update['new_cost'])
            else:
                ret = 'Adversary made an empty movement for edge {}, {}'.format(update['edge'][0],
                                                                                update['edge'][1])

        ret += '. Time left: {}'.format(time_left)
        return ret

    def full_state(self):
        return {
            'start_node': self.graph_map.start_node,
            'end_node': self.graph_map.end_node,
            'graph': self.graph_map.graph.adjacency_list
        }

    def switch_player(self):
        self.player[self.chance].switch_player()
        self.chance = (self.chance + 1) % 2
        self.player[self.chance].reset_timer()
