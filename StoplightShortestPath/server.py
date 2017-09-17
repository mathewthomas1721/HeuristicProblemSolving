#!/usr/bin/python           # This is server.py file
import sys
import socket               # Import socket module
from ssp import populateEdges
from ssp import showMoves
s = socket.socket()         # Create a socket object
populateEdges(sys.argv[1])
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   c.send('Message from server')
   showMoves(c.recv(1024))
   c.close()                # Close the connection