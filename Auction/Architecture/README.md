# HPS-AuctionGame
## Introduction
This repository contains code to run the Auction game. It includes a game manager, a server, and a client. The game allows more than two players to play in the same session.

## Rules
Each player starts out with 100 unit of money. There are <i>m</i> players, <i>k</i> artists, and <i>n</i> number of items that must be obtained. The server will generate one thousand items randomly from the group of artists. A player has to accumulate <i>n</i> of a type to win. The winning bid in each round is given by the player with highest bid. If multiple players offered the same highest bid, the winner will be the first player who sends the offer. Any invalid bid, such as insufficient fund, will cause the player to lose the game. All players will be told who won the bid and what they paid.

Here is an example (from course website):
Suppose there are two players (m = 2), four artists (k = 4), and the number of items that must be obtained is 3 (n = 3). 
Suppose that the first several items are: t2 t3 t4 t4 t4 t2 t3 t4 t2 t4 t2 t2 t2 t3 t4.

Consider the following history: 
player 1 wins t2 with 22 
player 1 wins t3 with 15 
player 0 wins t4 with 33 
player 0 wins t4 with 33

player 1 wins t4 with 34 
player 1 wins t2 with 22 
player 1 wins t3 with 0 
player 0 wins t4 with 8 and wins the game


## Game State
```
'finished': whether the game has finished
'auction_round': current auction round
'bid_item': auction item in this round
'bid_winner': winner in this round
'winning_bid': winning bid in this round
'remain_players': number of remaining players
```

## Client
A sample_client.py has been provided as reference. Client will receive the following initial states from server.

```
'artists_types': number of artists
'required_count': number of items for artist to win
'auction_items': list of auction items
'init_wealth': initial wealth per player
'player_count': number of players in the auction
```

## Get Started
```
To start auction game, run this script with the following arguments:
    ./start-game.py [-a <address> | -p <port> | -t <seconds>] m k n
    
where:
    a is the IP address to listen
    p is the port to run server on (Default: 9000)
    t is the game time in seconds (Default: 120)
    m is the number of players
    k is the number of artists
    n is the number of items that must be obtained
"""
```


