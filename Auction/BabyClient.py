#!/usr/bin/python
import atexit
import sys
from client import Client
import time
import random

def rankArtist(auctions, numArtists, req):
    allArtistRanks = []
    for x in range(len(req)):
        artistRanks = [0] * numArtists
        countArtist = [0] * numArtists
        for i in range(len(auctions)):
            curr_artist = int(auctions[i][1:])
            countArtist[curr_artist] += 1

            if countArtist[curr_artist] == req[x][curr_artist]:
                artistRanks[curr_artist] = i+1
        allArtistRanks.append(artistRanks)
    return allArtistRanks

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

def calculate_bid(ranks,item,curr_wealth, req):
    #print(curr_wealth)
    ourPlayer = ranks[0]
    rank1 = min(ourPlayer)
    ourRank1 = ourPlayer.index(rank1)
    #print ("Smallest Rank = " + str(rank1) + " for artist " + str(ourRank1))

    #if len(ranks) == 1:
    if item == ourRank1:
        if len(ranks) > 1:
            ranks = ranks[1:]
            ranks1 = []
            for x in ranks:
                ranks1.append(x.index(min(x)))
            indices = [i for i, x in enumerate(ranks1) if x == ourRank1]
            # all players (-1 index) whom we will be trying to outbid
            if len(indices)>0: # If there are any other players who want the item, outbid them
                maxProbableBid = 0
                for i in indices :
                    likelyBid = int(curr_wealth[i+1]/req[i+1][ourRank1])
                    print("HOW MUCH THEY CAN SPEND : " + str(curr_wealth[i+1]) + "\nHOW MANY THEY NEED : " + str(req[i+1][ourRank1]))
                    #likelyBid is how much they're likely to bid
                    if maxProbableBid < likelyBid:
                        maxProbableBid = likelyBid
                print("MAX PROBABLE BID = " + str(maxProbableBid))
                if maxProbableBid + 1 > int(curr_wealth[0]/2):
                    print("TOO HIGH, NOT BIDDING ")
                    return 0
                else:
                    print("OUR BID = " + str(maxProbableBid + 1) + " with a CURR_WEALTH = " + str(curr_wealth[0]) + " and " +str(req[0][ourRank1]) + " paintings needed")
                    return maxProbableBid + 1
            else: #otherwise place our standard bid
                print("OUR BID = " + str(int(curr_wealth[0]/req[0][ourRank1])) + " with a CURR_WEALTH = " + str(curr_wealth[0]) + " and " +str(req[0][ourRank1]) + " paintings needed")
                return int(curr_wealth[0]/req[0][ourRank1])
        else :
                pprint("OUR BID = " + str(int(curr_wealth[0]/req[0][ourRank1])) + " with a CURR_WEALTH = " + str(curr_wealth[0]) + " and " +str(req[0][ourRank1]) + " paintings needed")
                return int(curr_wealth[0]/req[0][ourRank1])
    else:
        return 0





if __name__ == '__main__':

    ip = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3]

    client = Client(name, (ip, port))
    atexit.register(client.close)

    artists_types = client.artists_types
    required_count = client.required_count
    auction_items = client.auction_items
    init_wealth = client.init_wealth
    player_count = client.player_count
    curr_wealth = [init_wealth] * player_count
    rem_auctions = auction_items
    req = []
    for i in range(player_count):
        req.append([required_count] * artists_types)
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
    playerNameDict = {name:0}
    while True:
        print("OUR CURRENT WEALTH = " + str(curr_wealth[0]))
        #print ("Entered round " + str(current_round))
        ranks = rankArtist(rem_auctions, artists_types, req)
        #print("RANKED")
        bid_amt = calculate_bid(ranks, int(rem_auctions[0][1:]), curr_wealth, req)
        #print ("BID GENERATED")
        client.make_bid(auction_items[current_round], bid_amt)
        #print ("BID SUBMITTED")
        # after sending bid, wait for other player
        game_state = client.receive_round()
        #print("GAME STATE RECEIVED")
        if game_state['bid_winner'] != None :
            if game_state['bid_winner'] not in playerNameDict:
                index = len(playerNameDict)
                playerNameDict[game_state['bid_winner']] = index

            #if game_state['bid_winner'] == name:
            curr_wealth[playerNameDict[game_state['bid_winner']]] -= game_state['winning_bid']
                #print("WE WON! UPDATING OUR WEALTH AND REQUIREMENTS!")
            #print(playerNameDict)
            req[playerNameDict[game_state['bid_winner']]][int(game_state['bid_item'][1:])] -= 1
        rem_auctions = rem_auctions[1:]
        check_game_status(game_state)
        #print("CHECKED IF FINISHED")
        current_round += 1
        #print("PROCEEDING TO ROUND " + str(current_round))
