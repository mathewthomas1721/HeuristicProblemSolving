def movingToward(hunterXPos,hunterYPos,hunterXVel,hunterYVel,preyXPos,preyYPos):
    relX = preyXPos - hunterXPos
    relY = preyYPos - hunterYPos
    return hunterXVel * relX >= 0 and hunterYVel * relY >= 0

#def findArea(hunterXPos,hunterYPos,walls,wallType)
#    if wallType = 1

def hunter(data):

    passplayerTimeLeft = data[0]
    gameNum = data[1]
    tickNum = data[2]
    maxWalls = int(data[3])
    wallPlacementDelay = data[4]
    boardsizeX = int(data[5])
    boardsizeY = int(data[6])
    currentWallTimer = int(data[7])
    hunterXPos = int(data[8])
    hunterYPos = int(data[9])
    hunterXVel = int(data[10])
    hunterYVel = int(data[11])
    preyXPos = int(data[12])
    preyYPos = int(data[13])
    numWalls = int(data[14])
    wallData = data[15:]
    i = 0
    walls = []
    while i<len(wallData):
        ind = int(wallData[i])
        tempWall = []
        if ind == 0:
            tempWall.append(ind)
            tempWall.append(int(wallData[i+1]))
            tempWall.append(int(wallData[i+2]))
            tempWall.append(int(wallData[i+3]))
            i = i+4
        elif ind == 1:
            tempWall.append(ind)
            tempWall.append(int(wallData[i+1]))
            tempWall.append(int(wallData[i+2]))
            tempWall.append(int(wallData[i+3]))
            i = i+4
        elif ind == 2:
            tempWall.append(ind)
            tempWall.append(int(wallData[i+1]))
            tempWall.append(int(wallData[i+2]))
            tempWall.append(int(wallData[i+3]))
            tempWall.append(int(wallData[i+4]))
            i = i+5
        elif ind == 3:
            tempWall.append(ind)
            tempWall.append(int(wallData[i+1]))
            tempWall.append(int(wallData[i+2]))
            tempWall.append(int(wallData[i+3]))
            tempWall.append(int(wallData[i+4]))
            i = i+5
        walls.append(tempWall)                
    print "WALLS"
    print walls
