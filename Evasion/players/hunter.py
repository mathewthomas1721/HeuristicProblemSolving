import math
import random
import numpy as np

minArea = -1
allPoints = []
for i in range(300):
    for j in range(300):
        allPoints.append((i,j))

def lineEqn(xPos,yPos,wallType):
    #print xPos,yPos,wallType
    if wallType == 0:

        eqn = [0,1,-yPos]

    elif wallType == 1:

        eqn = [1,0,xPos]

    elif wallType == 2:

        eqn = [1,-1,yPos-xPos]

    elif wallType == 3:

        eqn = [1,1,-yPos-xPos]

    return eqn

def sameSide(x1,y1,x2,y2,wallEqn):
    v1 = [x1,y1,1]
    v2 = [x2,y2,1]
    eqn1 = np.dot(v1,wallEqn)
    eqn2 = np.dot(v2,wallEqn)

    return eqn1 * eqn2 >= 0

def allPointsOnSameSide(x1,y1,wallEqn):
    points = []
    for i in range(300):
        for j in range(300):
            if sameSide(x1,y1,i,j,wallEqn):
                points.append((i,j))
    return set(points)

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

def distanceToWallEqn(XPos,YPos,wallEqn):
    return abs(np.dot([XPos,YPos,1],wallEqn)) / math.sqrt((wallEqn[0]**2) + (wallEqn[1]**2))

def findRestrictedArea(x1,y1,wallEqns):
    #print wallEqns
    pointSets = []

    '''for i in range(300):
        for j in range(300):
            allPoints.append((i,j))'''

    pointSets.append(set(allPoints))

    for eqn in wallEqns:
        pointSets.append(allPointsOnSameSide(x1,y1,eqn))
    area = set.intersection(*pointSets)
    return area;

def closestWallsEachType(game):
    min0 = 300
    min0wall = -1
    min1 = 300
    min1wall = -1
    min2 = 300
    min2wall = -1
    min3 = 300
    min3wall = -1
    for i in range(len(game.walls)):
        if game.walls[i][0] == 0:
            dist0 = distanceToWallEqn(game.preyXPos,game.preyYPos,game.wallEqns[i])
            if dist0 < min0:
                min0 = dist0
                min0wall = i
        elif game.walls[i][0] == 1:
            dist1 = distanceToWallEqn(game.preyXPos,game.preyYPos,game.wallEqns[i])
            if dist1 < min1:
                min1 = dist1
                min1wall = i
        elif game.walls[i][0] == 2:
            dist2 = distanceToWallEqn(game.preyXPos,game.preyYPos,game.wallEqns[i])
            if dist2 < min2:
                min2 = dist2
                min2wall = i

        elif game.walls[i][0] == 3:
            dist3 = distanceToWallEqn(game.preyXPos,game.preyYPos,game.wallEqns[i])
            if dist3 < min3:
                min3 = dist3
                min3wall = i
    send = []
    if min0wall!=-1:
        send.append(min0wall)
    if min1wall!=-1:
        send.append(min1wall)
    if min3wall!=-1:
        send.append(min2wall)
    if min3wall!=-1:
        send.append(min3wall)
    return send

class currGame:

    def __init__(self, data):
        self.passplayerTimeLeft = data[0]
        self.gameNum = data[1]
        self.tickNum = data[2]
        self.maxWalls = int(data[3])
        self.wallPlacementDelay = int(data[4])
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
        self.wallEqns = []
        #self.pointsOnSameSide=[]

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
                    self.wallEqns.append(lineEqn(tempWall[2], tempWall[1], ind))
                    i = i+4
                elif ind == 1:
                    tempWall.append(ind)
                    tempWall.append(int(wallData[i+1]))
                    tempWall.append(int(wallData[i+2]))
                    tempWall.append(int(wallData[i+3]))
                    self.wallEqns.append(lineEqn(tempWall[1], tempWall[2], ind))
                    i = i+4
                elif ind == 2:
                    tempWall.append(ind)
                    tempWall.append(int(wallData[i+1]))
                    tempWall.append(int(wallData[i+2]))
                    tempWall.append(int(wallData[i+3]))
                    tempWall.append(int(wallData[i+4]))
                    tempWall.append(int(wallData[i+5]))
                    self.wallEqns.append(lineEqn(tempWall[1], tempWall[3], ind))
                    i = i+6
                elif ind == 3:
                    tempWall.append(ind)
                    tempWall.append(int(wallData[i+1]))
                    tempWall.append(int(wallData[i+2]))
                    tempWall.append(int(wallData[i+3]))
                    tempWall.append(int(wallData[i+4]))
                    tempWall.append(int(wallData[i+5]))
                    self.wallEqns.append(lineEqn(tempWall[1], tempWall[3], ind))
                    i = i+6

                self.walls.append(tempWall) #parse wall data



def strat1(game):
    newWall = 0
    delWalls = ""
    #print len(findRestrictedArea(game.preyXPos,game.preyYPos,game.wallEqns))
    if movingToward(game):
        newWall = random.randint(1,4)
        newWallEqn = lineEqn(game.hunterXPos,game.hunterYPos,newWall-1)
        xPos = game.hunterXPos + game.hunterXVel
        yPos = game.hunterYPos + game.hunterYVel
        if not sameSide(xPos,yPos,game.preyXPos,game.preyYPos,newWallEqn):
            newWall = 0
    if len(game.walls) >= game.maxWalls-1:
        distances = []
        i = 0
        for wall in game.walls :
            dist = distanceToWall(game.preyXPos,game.preyYPos,wall) + distanceToWall(game.hunterXPos,game.hunterYPos,wall)
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

def strat2(game):
    global minArea
    if minArea == -1:
        minArea = len(findRestrictedArea(game.preyXPos,game.preyYPos,game.wallEqns))
    #print minArea
    bestWall = 0
    bestWallEqn = 0
    delWalls = ""
    for i in range(4):
        wallEqn = lineEqn(game.hunterXPos, game.hunterYPos, i)
        #print str(i) + " " + str(wallEqn)
        dist = distanceToWallEqn(game.preyXPos,game.preyYPos,wallEqn)
        if dist < game.wallPlacementDelay/2 and sameSide(game.hunterXPos, game.hunterXPos, game.preyXPos, game.preyYPos, wallEqn): #and movingToward(game):
            xPos = game.hunterXPos + game.hunterXVel
            yPos = game.hunterYPos + game.hunterYVel
            if sameSide(xPos, yPos, game.preyXPos, game.preyYPos, wallEqn):
                #print "CONDITIONS SATSIFIED"
                x = list(game.wallEqns)
                x.append(wallEqn)
                # ISSUE HERE
                area = len(findRestrictedArea(game.preyXPos,game.preyYPos,x))
                if area<minArea:
                    minArea = area
                    print str(area) + " " +str(i)
                    bestWall = i+1
                    bestWallEqn = wallEqn
    newWall = bestWall
    newWallEqn = bestWallEqn
    #print newWall


    '''game.walls.append(newWall)
    game.wallEqns.append(newWallEqn)'''
    closestWalls = closestWallsEachType(game)
    for i in range(len(game.walls)):
        if i not in closestWalls:
            delWalls = delWalls + str(i) + " "
    return str(newWall) + " " + str(delWalls)

def strat3(game):
    global minArea
    if minArea == -1:
        minArea = len(findRestrictedArea(game.preyXPos,game.preyYPos,game.wallEqns))
    #print minArea
    bestWall = 0
    bestWallEqn = 0
    delWalls = ""

    for i in range(4):
        wallEqn = lineEqn(game.hunterXPos, game.hunterYPos, i)
        #print str(i) + " " + str(wallEqn)
        dist1 = distanceToWallEqn(game.preyXPos,game.preyYPos,wallEqn)
        dist2 = math.hypot(game.preyXPos - game.hunterXPos, game.preyYPos - game.hunterYPos)
        if (dist1 < game.wallPlacementDelay/2) and sameSide(game.hunterXPos, game.hunterXPos, game.preyXPos, game.preyYPos, wallEqn): #and movingToward(game):
            xPos = game.hunterXPos + game.hunterXVel
            yPos = game.hunterYPos + game.hunterYVel
            if sameSide(xPos, yPos, game.preyXPos, game.preyYPos, wallEqn):
                #print "CONDITIONS SATSIFIED"
                x = list(game.wallEqns)
                x.append(wallEqn)
                # ISSUE HERE
                area = len(findRestrictedArea(game.preyXPos,game.preyYPos,x))
                if area<minArea:
                    minArea = area
                    print str(area) + " " +str(i)
                    bestWall = i+1
                    bestWallEqn = wallEqn
    newWall = bestWall
    newWallEqn = bestWallEqn



    if game.numWalls>game.maxWalls-3:
        delWalls = delWalls + "0 2 "


    return str(newWall) + " " + str(delWalls)

def strat4(game):
    global minArea
    if minArea == -1:
        minArea = len(findRestrictedArea(game.preyXPos,game.preyYPos,game.wallEqns))
    #print minArea
    bestWall = 0
    bestWallEqn = 0
    delWalls = ""

    if game.numWalls>game.maxWalls-3:
        delWalls = delWalls + "0 2 "


    return str(newWall) + " " + str(delWalls)

def preyStrat(game):
    '''x = list(game.wallEqns)
    x.append([0,1,-300])
    x.append([0,1,0])
    x.append([1,0,300])
    x.append([1,0,0])
    maxDist = 0
    for wall in x :
        dist = distanceToWallEqn(game.preyXPos,game.preyYPos,wall)
        if dist>maxDist:
            maxDist = dist
            yMov = wall[1]
            xMov = wall[0]'''


    if game.preyXPos > 150 :
        xMov = - random.randint(0,1)
    else :
        xMov = random.randint(0,1)

    if game.preyYPos > 150 :
        yMov = - random.randint(0,1)
    else :
        yMov = random.randint(0,1)

    return str(xMov) + " " + str(yMov)

def prey(data,strat):
    game = currGame(data)

    return preyStrat(game)

def hunter(data,strat):
    game = currGame(data)
    #print game.maxWalls
    if strat == 1:
        return strat1(game)
    elif strat == 2:
        return strat2(game)
    elif strat == 3:
        return strat3(game)
