## Architecture

This is only a brief overview of the architecture and gives
guidance for making any graph based games by extending this 
code.
In no way it should be taken that any game can be developed 
and one should evaluate their requirements before using 
this architecture.

## Overview

### Core

The [core](core) directory contains the main logic of the 
and contains the core algorithms to control the game.

- [graph.py](core/graph.py) contains the class for maintaining
a graph and a class GraphMapState which uses the graph as map
for travelling between given nodes and maintains the current
position of the agent on the map.

- [game_state.py](core/game_state.py) contains the main class
which maintains the state of the game and using the graph and
graph map. It maintains the player and call the appropriate
classes to make the moves and also gives the current state
as a dictionary.

- [player.py](core/player.py) contains the class player which
can be of two type as given in the enum inside. It makes moves
according to the type on the given graph.

- [game_looper.py](core/game_looper.py) contains a simple class
which runs the game as an infinite loop (until the game is 
over). It makes a open socket for all communications to 
happen and calls/updates the appropriate player about the
moves or state of the game. It is the controller class and 
knows how to call the appropriate class to run the game 
smoothly.

### connector

This directory contains files which helps in all the
communications between the server and bot clients. Both 
client and server uses json for easy serializing of
data to be sent over the socket.

- [server.py](connector/server.py) is the game server and opens
a socket where the client can connect and communicate with
the game.

- [client.py](connector/client.py) is the client class which
can be instantiated to talk to the game server and has 
some functions which are specific to this game which
ultimately call general functions for the communication

### sample
[Sample](sample) directory only contains sample files on 
how to use the clients and a sample game file.

## How to extend?
From my view, graph file can be kept constant if any game needs
a player moving on a graph while extending it only if 
extra functionality is needed. 
Player class can be changed to as it maybe changed based on
the type of players present and the constrained moves a
player can take.
Game state needs to be changed based on the game to maintain
the required information to run the game.
Game looper also will change based on how the game 
progresses with time.

The classes in connector are very much general and can be
extended based on the game for game specific communication.