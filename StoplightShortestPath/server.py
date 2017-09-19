#!/usr/bin/python
import os          
import sys
import socket     
import time          
from ssp import populateEdges
from ssp import showMoves
s = socket.socket()         
populateEdges(sys.argv[1])
host = socket.gethostname() 
port = 12345                
s.bind((host, port))  

f = open (sys.argv[1], "rb")
l = f.read()

s.listen(5)

while True:

   #send stoplight
   c, addr = s.accept()     
   c.sendall(l)

   #start timer
   t0 = time.time()
   moves = c.recv(1024)
   #print moves
   t1 = time.time()
   total = t1-t0
   #print total
   if total>120:
   		print "ERROR : OUT OF TIME"
   else:		
   		showMoves(moves)

   c.close()                # Close the connection
