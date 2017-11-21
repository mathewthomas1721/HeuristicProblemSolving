# Gravitational Voronoi

This repository contains the architect code for Gravitational Voronoi. It consists of a game server, a sample client, and a web visualization interface that displays the game progress in real time.

## The server

The server is written in Python 3. To run the server, execute:

```
python3 voronoi_game.py <number-of-stones> <number-of-players> <host-ip> <port> [<use-graphics>]
```

The last command line argument `<use-graphics>` is optional and graphics is only activated if you pass a `1` for this argument.

Also note that ports `10000` and `8080` are reserved for the web interface, so please use some other port. After all clients have connected, press `<Enter>` to start the game.

The server calculates the area of influence of each player discretely on a 1000 by 1000 grid. The final score of each player is the number of cells under the influence of that player.

## The client

In our implementation, there is no flag that indicates which client is the first (or second, etc.) player. Rather, player order is determined by the order in which each client connects to the server, i.e., the first client that connects to the server becomes the first player of the game. However, the play order (1-indexed) for each client will be sent upon successful connection.

In addition, player rotation after each game is built in, so that each player would play exactly one game as the first one to move. More details on how this works are included below.

A sample client in Python 3 is provided. To run the sample client, execute:

```
python3 voronoi_client.py <server-ip> <port> <team-name>
```

If you wish to write your own client, please follow the server-client communication protocol:

1. Connect your client to the server.

2. Receive game information. After connecting your client to the server, you should receive the game information from the server in the format of `"<number-of-players> <number-of-stones> <player-order>\n"`. The string is delimited by a space and ends with a new line character.

3. Send team name. After receiving the game information, you should send your team name to the server as a string.

4. Receive game updates. Your client will receive an update from the server when it is your turn. The update consists of three parts.
   1. Game over flag. The flag is set to `1` when the game is over, and `0` otherwise
   2. Scores. Say there are N players. Then there will be N numbers, representing the score from player 1 to player N.
   3. New moves. These are the moves that have been played after you played your last move. Each move consists of three numbers: the row of the move, the column of the move, and the player than made the move. The moves are ordered in the order in which they were played.

Notice that every number in the game update is separated by a space, and at the very end there will be a new line character.

The following represents what a general game update looks like. Note that the move row and move columns are **0-indexed**, and move players are **1-indexed**.

```
"<game-over-flag> <score1> <score2> ... <move1-row> <move1-col> <move1-player> <move2-row> <move2-col> <move2-player> ...\n"
```

5. Send move to server. After receiving a game update from the server, your client should finish your turn by sending a move to the server. The move should simply be a string `"<move_row> <move_col>"` - row and column of the move separated by a space.

A special note on the player rotation protocol - although multiple games are played during one competition (number of games equals number of players), the client needs to complete step `1-3` once only. Moreover, the server does not explicitly indicate the start of a new game. Instead, the client should check if the most recent update has the `game-over-flag` set, and if so, the client should treat all future updates as updates for a new game. It might be helpful to take a look at how the sample client handles rotation if the description is not clear enough.

## Running the game without display

To run the game without the display, run the server with:

```
python3 voronoi_game.py <number-of-stones> <number-of-players> <host-ip> <port>
```

and run each client with (if you are using the client provided here):

```
python3 voronoi_client.py <server-ip> <port> <team-name>
```

Finally, press `<Enter>` in the server terminal to start the game.

## Running the game with display

First you must make sure you have `node.js` and `npm` installed. You also need relatively modern versions of both `node.js` and the browser you will be using for the display, though nothing bleeding edge is needed. But if you encounter any errors, you should always try upgrading your browser/`node.js` first.

Now first install the single dependency (socket.io) if you haven't already:

```
npm install
```

To run the game with the display, first run the web server with

```
node web.js
```

and then open `localhost:10000` in your browser. You are now ready to run as many games as you want using basically the same approach as without a display. The only difference is to add a `1` to the server command from above like so:

```
python3 voronoi_game.py <number-of-stones> <number-of-players> <host-ip> <port> 1
```

Every time you start a new server the board will reset on your display.

### Saving boards from display
If you wish to save the boards (artworks) from the games you play you simply do exactly the same as above except you add a command line argument 1 to the web server as follows:

```
node web.js 1
```

and all the boards will be saved as PNG files in a folder which will be created if it doesn't already exist called artworks in the root of this project.
