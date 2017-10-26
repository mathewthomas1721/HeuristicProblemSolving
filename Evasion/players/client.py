
import socket
import random
import sys
import time
import random
import hunter

host = "172.16.42.248"
port = int(sys.argv[1])
strat = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

isHunter = False
stream = ""
while True:
    while True:
        stream = stream + sock.recv(4096)
        lines = stream.split("\n")
        if len(lines) > 1:
            line = lines[-2]
            stream = lines[-1]
            break
        else:
            continue

    #print "received: " + line

    val = .01
    time.sleep(val)

    tosend = None

    if line == "done":
        break
    elif line == "hunter":
        isHunter = True
    elif line == "prey":
        isHunter = False
    elif line == "sendname":
        tosend = "BabySnakes" + str(port)
    else:
        data = line.split(" ")
        #print len(data)
        if isHunter:


            move = hunter.hunter(data,strat)

            tosend = data[1] + " " + data[2] + " " + move
        else:

            #[gameNum] [tickNum] [x movement] [y movement]
            move = hunter.prey(data,strat)

            tosend = data[1] + " " + data[2] + " " + move

    if tosend is not None:
        #print "sending: " + tosend
        sock.sendall(tosend + "\n")
