import math
import random

class currGame:

    def __init__(self, data):
        self.passplayerTimeLeft = data[0]
        self.gameNum = data[1]
        self.tickNum = data[2]
        self.maxWalls = int(data[3])
        self.wallPlacementDelay = data[4]
        self.boardsizeX = int(data[5])
        self.boardsizeY = int(data[6])
        self.currentWallTimer = int(data[7])
        self.hunterXPos = int(data[8])
        self.hunterYPos = int(data[9])
        self.hunterXVel = int(data[10])
        self.hunterYVel = int(data[11])
        self.preyXPos = int(data[12])
        self.preyYPos = int(data[13])
        self.numWalls = int(data[14])
        self.walls = []
        wallData = data[15:]
        #print wallData
        i = 0
        if self.numWalls>0:
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
                    tempWall.append(int(wallData[i+5]))
                    i = i+6
                elif ind == 3:
                    tempWall.append(ind)
                    tempWall.append(int(wallData[i+1]))
                    tempWall.append(int(wallData[i+2]))
                    tempWall.append(int(wallData[i+3]))
                    tempWall.append(int(wallData[i+4]))
                    tempWall.append(int(wallData[i+5]))
                    i = i+6
                self.walls.append(tempWall) #parse wall data

def movingToward(game):
    relX = game.preyXPos - game.hunterXPos
    relY = game.preyYPos - game.hunterYPos
    '''if not (game.hunterXVel * relX >= 0 and game.hunterYVel * relY >= 0):
        print "FALSE"'''
    return game.hunterXVel * relX >= 0 and game.hunterYVel * relY >= 0

def distanceToWall(XPos,YPos,wall):
    ind = wall[0]

    if ind == 0:
        y1 = wall[1]
        y2 = wall[1]
        x1 = wall[2]
        x2 = wall[3]
    elif ind == 1:
        y1 = wall[2]
        y2 = wall[3]
        x1 = wall[1]
        x2 = wall[1]
    elif ind == 2:
        y1 = wall[3]
        y2 = wall[4]
        x1 = wall[1]
        x2 = wall[2]
    elif ind == 3:
        y1 = wall[3]
        y2 = wall[4]
        x1 = wall[1]
        x2 = wall[2]

    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)

    num = ((y2-y1)*XPos) - ((x2-x1)*YPos) + (x2*y1) - (x1*y2)
    num = abs(num)
    denom = math.sqrt(((y2-y1)**2) + ((x2-x1)**2))
    if denom == 0 :
        dist = 0
    else :
        dist = num/denom
    return dist

#def findArea(hunterXPos,hunterYPos,walls):

def strat1(game):
    newWall = 0
    delWalls = ""
    if movingToward(game):
        newWall = random.randint(1,4)
    if len(game.walls) >= game.maxWalls-1:
        distances = []
        i = 0
        for wall in game.walls :
            dist = distanceToWall(game.preyXPos,game.preyYPos,wall)
            distances.append((i,dist))
            i = i+1
        distances.sort(key=lambda tup: tup[1])
        #print distances
        delWalls = delWalls + str(distances[len(distances)-1][0])

        #delWalls + str(distances[game.maxWalls/2:][0])
        #print delWalls

    #    delWalls = delWalls + "0"
    #print str(newWall) + " " + str(delWalls)
    return str(newWall) + " " + str(delWalls)

def hunter(data,strat):
    game = currGame(data)
    print game.maxWalls
    if strat == 1:
        return strat1(game)
