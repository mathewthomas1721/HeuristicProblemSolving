# Stoplight Shortest Path Problem
## Game Description
The player is presented with a directed graph with each edge having a fixed traversal time. Each edge also has a color associated with it. Each color has a characteristic Green Time, during which the player may traverse an edge of that color, and a Red Time, during which the player may not traverse an edge of that color. If the player wants to cross the edge, he/she must traverse it ENTIRELY during the edge's Green Time, ie, a player cannot start crossing during Green Time if they cannot complete the traversal during Green Time. A player may wait until an appropriate time during which they can make a legal traversal. The goal is to find the shortest path between two nodes

## Rule Violations
1. Traversing an edge outside of its Green Time
2. Listing a traversal as taking more/less time than is required
3. Traversing an edge that does not exist
4. Traversing an edge that is not connected to the endNode of the previous traversal

## Input and Output
The server will provide the player with a file containing all the edges in the graph. The file will also contain specifications for each particular color. The format of the file would be as follows : 

node1 node2 color traversetime
color greentime redtime 

Both will be in a single file.

The player must return a sequence of edge traversals along with a start and end time for each traversal. The player will have a maximum of 2 minutes to generate their traversals. The server will parse through the edges, check for violations, and return the traversal time of a valid path. ALL the edge traversals should be returned in the form of a single string in the following format :

startNode endNode startTime endTime

Each traversal should be separated by a line break. 

## Working
If you're using Python, then import the Client class utilize the recv_stoplight() function to receive the stoplight file from the server and send_resp() function to send the traversals you've generated to the server. Please note, this platform is written in Python2, so there may be some difficulties for Python3 users.

If you're not using Python, you have two options :

1. Write your own Client to interact with the server
2. Use the wrapper functions provided (see below), to interact with the client through stdin

## Classes
### Client Class
To initialize a new Client object, use the following statement :

	client = Client(serv_addr,port)

*serv_addr* is the IP address of the server

*port* is the relevant port

Default port value is 12345	

#### recv_stoplight()
Receives the stoplight file from the server.
#### send_resp()
Sends the generated moves to the server.
#### wrap_recv()
Wrapper function for recv_stoplight(), prints to stdout
#### wrap_send()
Wrapper function for send_resp(), reads from stdin


