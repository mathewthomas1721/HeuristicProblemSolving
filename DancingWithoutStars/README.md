Dancing without Stars
=====================

## Details
On a `N x N` checker board, there are `c` groups of dancers in their initial positions. Each group will have a unique color and each group have `k` dancers.  

The choreographer is going to ask the dancers to make moves. The goal of the choreographer is to ensure that there are disjoint, contiguous vertical or horizontal line segments of dancers.  

For example, there are color `1`, `2`, `3`, `4`, and `k = 3`, then the following is a valid final state:
```
1234  2
      1
  42133
      4
```
They can be in any order, but one line should contain exactly one dancer of each color.  
A line can touch another line but they must be disjoint which means they can't share any dancer.  

The spoiler is going to place `k` stars on the board before choreographer starts to move, and try make choreographer to spend more steps to reach a final state.

Both players will have `120` seconds as thinking time.

## Choreographer
Choreographer will connect to server first and send their name to the server.  
Server will send an `input_file` to choreographer. An `input_file` is similiar to `sample_dancedata.txt`.  

Server will then send some other parameters to Choreographer:  
`<board_size> <num_of_color> <k>`

After spoiler has placed all the stars, server will send choreographer all the stars in the following format:  
`<star_1_x> <star_1_y> <star_2_x> <star_2_y> ..... <star_k_x> <star_k_y>`  

The server will start counting time immediately after sending stars.  

The choreographer needs to send steps of parallel moves to the server. One `step` contains multiple `parallel move`s. Those dancers like to move at the same time that's why it's called "parallel". However, one dancer cannot move twice within one `step`. And no dancer can move on to a star. They can only move to an empty position or swap positions. And note, each dancer can only move 1 row-wise or col-wise so the manhattan distance between the start point and the end point should be 1.

Choreographer needs to send the steps one by one to the server in the following format:  
`<num_of_moves> <move1_start_x> <move1_start_y> <move1_end_x> <move1_end_y> ... <moveK_start_x> <moveK_start_y> <moveK_end_x> <moveK_end_y>`

Choreographer needs to send a flag `DONE` to the server when all the steps are sent.  
The last step for Choreographer is to send all the lines to the server in the following format:  
`line1_start_x line1_start_y line1_end_x line1_end_y ...`

The clock will stop counting once you sent "DONE" to server, but server will validate if line info matches steps later.

## Spoiler
Spoiler will be the second to connect to the server and send their name to the server.  
Server will send the `input_file` such like `sample_dancedata.txt` to the spoiler first.  

Server will then send the other parameters to spoiler same as what server will do to choreographer:  
`<board_size> <num_of_color> <k>`

The spoiler needs to send stars to the server in the following format:  
`<star_1_x> <star_1_y> <star_2_x> <star_2_y> ..... <star_k_x> <star_k_y>`  

Stars can only be placed on an empty spot. And no two stars can be closer then `c + 1` manhattan distance apart. Where `c` is the number of colors.  

Manhattan distance: `|x1 - x2| + |y1 - y2|`.  

And then spoiler can rest.

## IMPORTANT NOTE If you are making your own client
Every time when you send something to server, make sure to append an `&` to the end of your string.  
This means the end of some data to the server.  

And when server send something back, it will have an `&` at the end too. Make sure to handle that.  

## Run the server
```bash
python3 game.py -H <host> -p <port> -f <filename> -s <size>
```  
Where `size` means the board size.

## Run the sample player
For Choreographer
```bash
python3 sample_player.py -H <host> -p <port> -s
```
For spoiler
```bash
python3 sample_player.py -H <host> -p <port> -c
```

Both uses randomized methods, so sample choreographer can hardly reach the goal.

## Scoring
Two players will play as choreographer and spoiler in turns.  
The player who make an invalid move will lose that round.
If each player lost a round then its a draw.  
If no one made any invalid move then the one choreographer who uses fewer steps will win.

## Graphic Interface
In order to run UI display, you need to install some requirements.  
First install node dependencies:
```bash
npm install
```
Then install one python dependency:
```bash
pip install requests
```
Now you can run the node server using:
```bash
node index.js
```
And go to `127.0.0.1:3000` in your browser. I hardcoded the ip and port...  
Then start the game as normal except adding one more option `-u` at the end.  

With display mode, executing/validating move stage will run a bit slower so that it can be observed by human.

## Contact
Let me know if there is any bugs or problems.  
`taikun@nyu.edu`
