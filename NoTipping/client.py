import socket
import sys
import random
from board import Board
from noTip import alpha_beta_search
import copy




HOST = sys.argv[1].split(":")[0]
PORT = int(sys.argv[1].split(":")[1])              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
myWeight = dict()

first = 0
name = "BabySnakes"

for idx, val in enumerate(sys.argv):
    if(val == "-f"): 
        first = 1
    if(val == "-n"):
        name = sys.argv[idx + 1]
s.sendall('{} {}'.format(name, first))


k = int(s.recv(1024))
print "Number of Weights is: " + str(k)

for i in range(1, k):
    myWeight[i] = i;
oldBoard = Board(k)
newBoard = -1
diffr = -1
while(1):
    data = s.recv(1024) # get the data
    data = [int(data.split(' ')[i]) for i in range(0, 63)]

    
    if data[62] == 1: # checks the 62nd board position (?), ie, checks if finished
        break
    if newBoard != -1:
    	oldBoard = copy.deepcopy(newBoard)
    board = data[1:-1]

    for i in range(len(oldBoard.board)):
    		if board[i] != oldBoard.board[i]:
    			diffr = board[i]
    #oldBoard.oppBlocks[diffr-1] = 0			
    oldBoard.board = board  
    #print ol

    print "CURRENT BOARD = \n" + str(oldBoard.board) + "\n"
    print "OUR WEIGHTS = \n" + str(oldBoard.myBlocks) + "\n"
    print "THEIR WEIGHTS = \n" + str(oldBoard.oppBlocks) + "\n"

    if data[0] == 0:
    	if diffr != -1:
    		oldBoard.oppBlocks[diffr-1] = 0
    	newBoard = alpha_beta_search(oldBoard,0)
    	#print oldBoard.board
    	#print newBoard.board
    	for i in range(len(newBoard.board)):
    		if newBoard.board[i] != oldBoard.board[i]:
    			diff = newBoard.board[i]

    	ind = newBoard.board.index(diff)-30
    	print "OUR MOVE = "
    	print "Added: (" + str(diff) + "," + str(ind) + ")\n" 
    	print "NEW BOARD = \n" + str(newBoard.board) + "\n"
        s.sendall('{} {}'.format(diff, ind))

        #board = newBoard

    else:
    	if diffr != -1:
    		oldBoard.oppBlocks[diffr-1] = 0
    	newBoard = alpha_beta_search(oldBoard,1)
    	#print oldBoard.board
    	#print newBoard.board
    	for i in range(len(newBoard.board)):
    		if newBoard.board[i] != oldBoard.board[i]:
    			diff = oldBoard.board[i]

    	ind = newBoard.board.index(diff)-30
    	print "OUR MOVE = "
    	print "Removed: (" + str(diff) + "," + str(ind) + ")" 
    	print "NEW BOARD = \n" + str(newBoard.board) + "\n"
        s.sendall('{}'.format(diff))
    	#print " can't do it yet "#"Removed:" + str(choice)
        #s.sendall('{}'.format(choice))

s.close()            