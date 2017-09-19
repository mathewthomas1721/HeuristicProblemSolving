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

   
   t0 = time.time() #start timer
   moves = c.recv(1024)
   t1 = time.time() #end timer

   total = t1-t0
   
   if total>120:
   		print "ERROR, OUT OF TIME : " + str(total)
   else:		
   		showMoves(moves)

   c.close()                # Close the connection
