# Echo client program
import socket
import sys
import random

HOST = sys.argv[1].split(":")[0]
PORT = int(sys.argv[1].split(":")[1])              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
myWeight = dict()

first = 0
name = "theRons"

for idx, val in enumerate(sys.argv):
    if(val == "-f"): 
        first = 1
    if(val == "-n"):
        name = sys.argv[idx + 1]
s.sendall('{} {}'.format(name, first))


k = int(s.recv(1024))
print "Number of Weights is: " + str(k)

for i in range(1, k):
    myWeight[i] = 1;

def check_balance(board):
    left_torque = 0
    right_torque = 0
    for i in range(0,61):
        left_torque += (i - 30 + 3) * board[i]
        right_torque += (i - 30 + 1) * board[i]
    left_torque += 3 * 3
    right_torque += 1 * 3
    return left_torque >= 0 and right_torque <= 0


def find_place_position(key, board):
    for i in range(0,61):
        if board[i] == 0:
            board[i] = key
            if check_balance(board):
                board[i] = 0
                return i
            board[i] = 0
    return -100

while(1):
    data = s.recv(1024) # get the data
    while not data: # checks if data was received
        continue

    data = [int(data.split(' ')[i]) for i in range(0, 63)] # splits the string into data
    print data
    board = data[1:-1] # constructs the board out of the data
    check_balance(board) # checks whether the board is balanced
    #print board
    if data[62] == 1: # checks the 62nd board position (?)
        break

    if data[0] == 0:  # I think this is a check to see if the board is set for removal or placement of weights
        allPosition = []
        for key,value in myWeight.iteritems():
            if value == 1:
                position = find_place_position(key, board)
                if position != -100:
                    allPosition.append((key, position - 30))
                if position != -100:
                    allPosition.append((key, position - 30))
                    break
        if len(allPosition) == 0:
            choice = (1, 0)
        else:
            choice = random.choice(allPosition)
        myWeight[choice[0]] = 0
        print "Added: " + str(choice)
        s.sendall('{} {}'.format(choice[0], choice[1]))

    else:
        allPossiblePosition = []
        for i in range(0, 61):
            if board[i] != 0:
                tempWeight = board[i]
                board[i] = 0
                if check_balance(board):
                    allPossiblePosition.append(i - 30)
                board[i] = tempWeight
        if len(allPossiblePosition) == 0:
            choice = (1)
        else:
            choice = random.choice(allPossiblePosition)
            random.jumpahead(1);
        print "Removed:" + str(choice)
        s.sendall('{}'.format(choice))


s.close()
