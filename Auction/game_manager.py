from datetime import datetime
import json
import random
from server import Server

class Player:

    def __init__(self, name, wealth, time):
        self._dict = {'name': name,
                      'wealth': wealth,
                      'remain_time': time,
                      'valid': True,
                      'reason': ""}

        self.prev_time = None

    def __setitem__(self, key, value):
        if key not in self._dict:
            raise KeyError('Key %s is not defined.' % key)

        self._dict[key] = value

    def __getitem__(self, item):
        return self._dict[item]

class AuctionManager:

    def __init__(self, num_players, required_count, num_artists, player_wealth=100,
                 game_time=120, address='', port=9000):

        """
        :param num_players: number of players
        :param num_artists: number of artists
        :param required_count: number of items that must be obtained to win
        :param game_time: 120 sec (2 min) per player
        :param address: host server address
        :param port: host server port (default: 8000)
        """

        self.players = []

        for idx in range(num_players):
            self.players.append(Player(idx, player_wealth, game_time))

        self.__player_count = num_players
        self.__required_count = required_count
        self.__init_wealth = player_wealth
        self.__artists_types = num_artists

        self.item_types = []
        self.bid_winners = dict()

        for artist_id in range(num_artists):
            item_id = 't' + str(artist_id)
            self.item_types.append(item_id)
            self.bid_winners[item_id] = [0 for x in range(num_players)]

        self.auction_items = []

        type_count = len(self.item_types)

        for i in range(1000):
            rand_item = self.item_types[int(type_count * random.random())]
            self.auction_items.append(rand_item)

        self.__game_state = {'finished': False,
                             'winner': None,
                             'reason': None,
                             'bid_item': None,
                             'bid_winner': None,
                             'auction_round': 0,
                             'remain_players': num_players,
                             }

        for idx in range(len(self.players)):
            player_name = self.get_player_name(idx)
            self.__game_state[player_name] = self.players[idx]

        self.__over = False
        self.__time_limit = game_time
        self.__prev_time = None
        self.__server = Server(address, port, self.__player_count)
        self.__log = open('game-log.txt', 'w+')

    def run_game(self):
        """
        Starts auction game
        """

        data = self.__server.establish_connection()
        players_data = list(map(lambda x: json.loads(x.decode('utf-8')), data))

        for idx in range(len(self.players)):
            self.players[idx]['name'] = players_data[idx]['name']

        self.__server.update_all_clients(
            bytes(json.dumps({'artists_types': self.__artists_types,
                              'required_count': self.__required_count,
                              'init_wealth': self.__init_wealth,
                              'auction_items': self.auction_items,
                              'player_count': self.__player_count}), 'utf-8'), self.get_valid_players())

        auction_round = 0

        while self.__game_state['remain_players'] > 0:
            # self.reset_players_timer() # start timer
            remain_times = self.get_player_remain_time()

            next_bids = self.__server.receive_any(remain_times)

            game_state = self.handle_bids(auction_round, next_bids)
            game_state_bytes = bytes(json.dumps(game_state), 'utf-8')

            self.__server.update_all_clients(game_state_bytes, self.get_valid_players())

            if game_state['finished']:
                self.close()
                exit(0)
            else:
                auction_round += 1

    def handle_bids(self, auction_round, bids):
        """
        Handle game_state and error checking on bids
        :param self:
        :param auction_round:
        :param bids:
        :return:
        """

        game_state = dict()
        game_state['finished'] = False

        if self.__over:
            # Game is already over
            game_state.update(self.__game_state)

        else:
            max_bid = dict()
            max_bid['amount'] = 0
            max_bid['bidder'] = None
            max_bid['received_time'] = None

            bid_item = self.auction_items[auction_round]

            for idx in range(len(bids)):
                player_id = bids[idx]['player']

                if self.players[player_id]['valid'] is False: # skip invalid players
                    continue

                elif bids[idx]['timeout'] is True: # player was timed out during bidding
                    self.players[player_id]['valid'] = False
                    self.players[player_id]['remain_time'] = -1
                    print(('Player {} was timed out on round {}.'
                           .format(self.players[player_id]['name'], auction_round)))

                    continue

                start_time = bids[idx]['start_time']
                received_time = bids[idx]['received_time']
                bid_summary = bids[idx]['bid']

                # handle timestamp checking
                self.players[player_id]['remain_time'] -= (received_time - start_time).total_seconds()

                if self.players[player_id]['wealth'] - bid_summary['bid_amount'] >= 0:

                    bid_amt = bid_summary['bid_amount']

                    # highest bidder or first bidder (if same bid amount)
                    if bid_amt > max_bid['amount'] or (bid_amt == max_bid and max_bid['amount'] > 0 and
                                                               received_time < max_bid['received_time']):
                        max_bid['amount'] = bid_amt
                        max_bid['bidder'] = player_id
                        max_bid['received_time'] = received_time

                else:
                    # invalid bid from player
                    self.players[player_id]['valid'] = False
                    print('Player {} made an invalid bid on round {}.'
                          .format(self.players[player_id]['name'], auction_round))

            max_bidder = max_bid['bidder']

            if max_bid['amount'] > 0 and max_bidder is not None:

                self.players[max_bidder]['wealth'] -= max_bid['amount']
                self.bid_winners[bid_item][max_bidder] += 1

                if self.bid_winners[bid_item][max_bidder] >= self.__required_count:
                    game_state['finished'] = True
                    game_state['winner'] = max_bidder  # wins
                    game_state['reason'] = ('Player {} won the game! Congrats!'
                                            .format(self.players[max_bidder]['name']))

            game_state['bid_item'] = self.auction_items[auction_round]

            if max_bidder is not None:
                game_state['bid_winner'] = str(self.players[max_bidder]['name'])
            else:
                game_state['bid_winner'] = None

            game_state['winning_bid'] = max_bid['amount']
            game_state['auction_round'] = auction_round

            remain_player_count = 0
            for idx in range(len(self.players)):
                player_name = self.get_player_name(idx)
                game_state[player_name] = self.players[idx]._dict

                if self.players[idx]['valid'] is True:
                    remain_player_count += 1

            game_state['remain_players'] = remain_player_count

            if remain_player_count == 0:
                # game ends
                game_state['finished'] = True
                game_state['reason'] = 'No valid players remaining'

            if auction_round == len(self.auction_items) - 1 and game_state['finished'] is False:
                # last round and no winner, then set game to finished
                game_state['finished'] = True
                game_state['reason'] = 'Draw Game. Out of Auction Items.'


            self.__game_state.update(game_state)
            self.__over = game_state['finished']
            self.print_status(game_state, auction_round)

        return game_state

    def get_player_remain_time(self):
        remain_times = dict()

        for idx in range(len(self.players)):
            player_remain_time = self.players[idx]['remain_time']

            if player_remain_time > 0 and self.players[idx]['valid'] is True:
                remain_times[idx] = player_remain_time
            else:
                remain_times[idx] = 0

        return remain_times

    def get_valid_players(self):
        valid_players = dict()

        for idx in range(len(self.players)):
            valid_players[idx] = self.players[idx]['valid']

        return valid_players

    def print_status(self, state, auction_round):
        """Prints game status after each round"""

        if state['bid_winner'] is None:
            self.log('No bidder on this round {}.\n'.format(auction_round))
        else:
            self.log('Player {} won {} on this round {} with bid amount {}.\n'.format(
                state['bid_winner'], state['bid_item'], auction_round, state['winning_bid']))

        self.log('Remaining time:')
        for idx in range(len(self.players)):
            if self.players[idx]['valid']:
                self.log('\t{} has {} seconds remaining'
                         .format(self.players[idx]['name'], self.players[idx]['remain_time']))

        self.log('Remaining wealth:')
        for idx in range(len(self.players)):
            if self.players[idx]['valid']:
                self.log('\t{} has {} dollars remaining'.format(self.players[idx]['name'], self.players[idx]['wealth']))

        self.log('------------------------------------\n')

        if state['finished']:
            self.log('Game over\n{}\n'.format(state['reason']))

    def get_player_name(self, player_id):
        return 'player_' + str(player_id)

    def log(self, message):
        print(message)
        self.__log.write(message)

    def __del__(self):
        self.close()

    def close(self):
        self.__log.close()
        self.__server.close()