#!/usr/bin/python
import atexit
import sys
from client import Client
import time
import random

def rankArtist(auctions, numArtists, req):
    artistRanks = [0] * numArtists
    countArtist = [0] * numArtists
    for i in range(len(auctions)):
        curr_artist = int(auctions[i][1:])
        countArtist[curr_artist] += 1

        if countArtist[curr_artist] == req[curr_artist]:
            artistRanks[curr_artist] = i
    return artistRanks

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

def calculate_bid(ranks,item,curr_wealth):
    rank1 = min(ranks)
    if item == ranks.index(rank1):
        if rank1>0:
            return int(curr_wealth/rank1)
        else :
            return curr_wealth
    else:
        return 0

if __name__ == '__main__':

    ip = sys.argv[1]
    port = int(sys.argv[2])

    client = Client('BabySnakes', (ip, port))
    atexit.register(client.close)

    artists_types = client.artists_types
    required_count = client.required_count
    auction_items = client.auction_items
    init_wealth = client.init_wealth
    player_count = client.player_count
    curr_wealth = init_wealth
    rem_auctions = auction_items
    req = [required_count] * artists_types
    '''print ("RANKS")
    print(rankArtist(auction_items, artists_types, required_count))'''
    '''print ("artists_types")
    print (artists_types)
    print ("required_count")
    print (required_count)
    print ("auction_items")
    print (auction_items)
    print ("init_wealth")
    print (init_wealth)'''
    current_round = 0

    while True:

        ranks = rankArtist(rem_auctions, artists_types, req)
        bid_amt = calculate_bid(ranks, int(rem_auctions[0][1:]), curr_wealth)
        client.make_bid(auction_items[current_round], bid_amt)

        # after sending bid, wait for other player
        game_state = client.receive_round()
        if game_state['bid_winner'] == 'BabySnakes':
            curr_wealth = curr_wealth - game_state['winning_bid']
            req[int(game_state['bid_item'][1:])] -= 1
        rem_auctions = rem_auctions[1:]
        check_game_status(game_state)

        current_round += 1
