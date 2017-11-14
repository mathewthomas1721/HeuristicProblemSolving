#!/usr/bin/python

"""
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

from getopt import getopt
import sys

from game_manager import AuctionManager

if __name__ == '__main__':
    try:
        opts, args = getopt(sys.argv[1:], 'a:m:p:t:')

    except GetoptError:
        sys.stderr.write('Error: parsing arguments\n')
        sys.stderr.write(__doc__)
        exit(-1)

    time = 120
    port = 9000
    address = ''
    player_count = 2

    for o, a in opts:
        if o == '-a':
            address = a
        elif o == '-p':
            port = int(a)
        elif o == '-t':
            time = int(a)

    try:
        player_count = int(args[0])
        num_artists = int(args[1])
        required_count = int(args[2])

    except (IndexError, ValueError):
        sys.stderr.write(__doc__)
        exit(-1)

    auction_manager = AuctionManager(player_count, required_count, num_artists,
                                     game_time=time, address=address, port=port)

    auction_manager.run_game()
