import apiInteract as api
import sys
import subprocess
import json
#from time import localtime, strftime
import datetime


'''

0 for creating a contest

1 to register for a contest

2 for poser functionality

3 for solver functionality

Not going to implement 2 and 3 because we have the client for that

'''

op = int(sys.argv[1])
id1 = -1
name = 'FalqanSpawn'
path = 'linserv1.cims.nyu.edu:34567'
# args : numpackages, numversions, numcompatibles
if op == 0:
    rightNow = datetime.datetime.now()
    poserTime = rightNow + datetime.timedelta(hours=2)
    solverTime = rightNow + datetime.timedelta(hours=4)
    rightNow = rightNow.strftime("%m/%d/%Y %I:%M:%S %p")
    poserTime = poserTime.strftime("%m/%d/%Y %I:%M:%S %p")
    solverTime = solverTime.strftime("%m/%d/%Y %I:%M:%S %p")
    x = api.createGame(path,rightNow, poserTime,solverTime, sys.argv[2], sys.argv[3], sys.argv[4])
    y = str(x.text)
    #print(y)
    id1 = int(y[1:len(y)-1].split(',')[1].split(':')[1])
    print("CONTEST CREATED : " + str(id1))
    op = 1
 # args : contest id
if op == 1:
    if id1 == -1:
        id1 = int(sys.argv[2])
    x = api.registerAGame(path,id1, name)
    a = str(x.text)
    accesscode = int(a[1:len(a)-1].split(',')[1].split(':')[1])
    print(name + " REGISTERED FOR CONTEST " + str(id1) + "\nACCESS CODE : " + str(accesscode))
    jsondat = {"id": id1,"pid": name,"code": accesscode,"hostname": "linserv1.cims.nyu.edu","port": 34567,"_comment": "id: Contest ID; pid: Problem Name; code: Your Access Code"}

    with open('client.json', 'w') as outfile:
        json.dump(jsondat, outfile)

if op == 2:
    with open('client.json', 'r') as f:
        json_data = json.load(f)
        json_data["pid"] = name

    with open('client.json', 'w') as f:
        f.write(json.dumps(json_data))

    subprocess.call('./setup.sh && ./client.js poser', shell=True)

# args : PoserID
if op == 3:
    with open('client.json', 'r') as f:
        json_data = json.load(f)
        json_data["pid"] = sys.argv[2]

    with open('client.json', 'w') as f:
        f.write(json.dumps(json_data))


    subprocess.call('./setup.sh && ./client.js solver', shell=True)
