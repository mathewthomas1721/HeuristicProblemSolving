#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = '67.244.31.93' #socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
print s.recv(1024)
f = open ("moves", "rb")
l = f.read(1024)
s.send('moves')
s.close                     # Close the socket when done
