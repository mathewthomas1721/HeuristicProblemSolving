from collections import defaultdict

def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item

def sort_and_deduplicate(l):
    return list(uniq(sorted(l)))

def checkFinished(curr,final):
    for i in range(len(curr)):
        if curr[i] != final[i]:
            return False
    return True

def whichFinished(curr,final):
    finished = []
    for i in range(len(curr)):
        if curr[i] == final[i]:
            finished.append(curr[i])
    return finished

def horizontalMove(initial, final, allPrev, stars):
    retVal = list(initial) #set returnVal to initial
    if initial[0] < final[0]: #check whether to move right
        retVal[0] = initial[0] + 1
    else :                    #otherwise, move left
        retVal[0] = initial[0] - 1
    print retVal
    if ((retVal in allPrev) or (retVal in stars)): #check if that move is to an occupied or starred square
        if (initial[1] != final[1]): #if so, check if we can make a vertical move
            retVal = list(verticalMove(initial,final,allPrev,stars))
        else : #if we can't make a vertical move
            retVal = list(initial)
            if retVal in stars : #we can't wait, since the square won't change
                if retVal[1] >= 0 or retVal[1] < 48:
                    retVal[1] = retVal[1] + 1
                else:
                    retVal[1] = retVal[1] - 1
        print retVal
        if retVal in allPrev :
            print "STILL CAN'T INSERT THAT SO, SIT DOWN "
            retVal = list(initial)
    return retVal

def verticalMove(initial, final, allPrev, stars):
    retVal = list(initial) #set returnVal to initial
    if initial[1] < final[1]: #check whether to move up
        retVal[1] = initial[1] + 1
    else :                    #otherwise, move down
        retVal[1] = initial[1] - 1
    print "VALUE TO INSERT"
    print retVal
    if ((retVal in allPrev) or (retVal in stars)): #check if that move is to an occupied or starred square
        print "CAN'T INSERT THAT SO, INSERT THIS : "
        if (initial[0] != final[0]): #if so, check if we can make a horizontal move
            retVal = list(horizontalMove(initial,final,allPrev,stars))
        else : #if we can't make a horizontal move
            retVal = list(initial)
            if retVal in stars : #we can't wait, since the square won't change
                if retVal[0] >= 0 or retVal[0] < 48:
                    retVal[0] = retVal[0] + 1
                else:
                    retVal[0] = retVal[0] - 1
        print retVal
        if retVal in allPrev :
            print "STILL CAN'T INSERT THAT SO, SIT DOWN "
            retVal = list(initial)

    return retVal

'''def horizontalMoveNew(initial, final, unfinished, finished, stars):
    retVal = list(initial) #set returnVal to initial
    if initial[0] < final[0]: #check whether to move right
        retVal[0] = initial[0] + 1
    else :                    #otherwise, move left
        retVal[0] = initial[0] - 1
    print retVal

    if retVal in stars:
        retVal = list(verticalMoveNew(initial, final, unfinished, finished, stars))
    elif retVal in finished:

    return retVal

def verticalMoveNew(initial, final, unfinished, finished, stars):
    retVal = list(initial) #set returnVal to initial
    if initial[1] < final[1]: #check whether to move up
        retVal[1] = initial[1] + 1
    else :                    #otherwise, move down
        retVal[1] = initial[1] - 1
    print retVal

    return retVal'''

def viableHorizontalMove(initial,final):

    positive = list(initial)
    positive[0] = positive[0] + 1
    negative = list(initial)
    negative[0] = negative[0] - 1
    if initial[0] < final[0]:
        moves = [positive,negative]
    else:
        moves = [negative,positive]

    return moves

def viableVerticalMove(initial,final):
    positive = list(initial)
    positive[1] = positive[1] + 1
    negative = list(initial)
    negative[1] = negative[1] - 1
    if initial[1] < final[1]:
        moves = [positive,negative]
    else:
        moves = [negative,positive]

    return moves

def pathCost1(initialPos, finalPos, stars):
    cost = 0
    skip = []
    while not checkFinished(initialPos,finalPos):
        print "\n\nCURRPOS"
        print initialPos
        print "SKIP"
        print skip
        for i in range(len(initialPos)):
            print initialPos[i]
            if initialPos[i] != finalPos[i]:
                if initialPos[i][0] != finalPos[i][0] : # Horizontal Movement
                    if i in skip:
                        skip.remove(i)
                    else:
                        if initialPos[i][0] < finalPos[i][0]:
                            test = initialPos[i]
                            test[0] = test[0] + 1
                            if test in stars:

                                if test[1]<=finalPos[i][1]:
                                    test[1] = test[1] + 1
                                else:
                                    test[1] = test[1] - 1

                                test[0] = test[0] - 1


                        else :
                            test = initialPos[i]
                            test[0] = test[0] - 1
                            if test in stars:

                                if test[1]<=finalPos[i][1]:
                                    test[1] = test[1] + 1
                                else:
                                    test[1] = test[1] - 1

                                test[0] = test[0] + 1
                        initialPos[i] = test
                else:
                    if initialPos[i][1] < finalPos[i][1]:
                        test = initialPos[i]
                        test[1] = test[1] + 1
                        if test in stars:
                            test[0] = test[0] + 1
                            #test[1] = test[1] - 1
                            skip.append(i)

                    else :
                        test = initialPos[i]
                        test[1] = test[1] - 1
                        if test in stars:
                            test[0] = test[0] + 1
                            #test[1] = test[1] + 1
                            skip.append(i)
                    initialPos[i] = test                                   # Vertical Movement
        cost = cost + 1

    return cost

def pathCost2(initialPos, finalPos, stars):
    cost = 0
    while not checkFinished(initialPos,finalPos):
        #print initialPos
        #print finalPos
        for i in range(len(initialPos)):
            prev = list(whichFinished(initialPos,finalPos)) + initialPos[:i]
            print "\n\nVALUES WE CAN'T INSERT"
            print prev
            if initialPos[i] != finalPos[i]:
                if initialPos[i][0] != finalPos[i][0]:
                    initialPos[i] = list(horizontalMove(initialPos[i],finalPos[i],prev,stars))
                else:
                    initialPos[i] = list(verticalMove(initialPos[i],finalPos[i],prev,stars))
        cost = cost + 1
        print "\n\nAT THE END OF THIS ROUND, POSITIONS ARE : "
        print initialPos
    return cost

def pathCost3(initialPos, finalPos, stars):
    while not checkFinished(initialPos,finalPos):
        moves = []
        for i in range(len(initialPos)):
            horiz = viableHorizontalMove(initialPos[i],finalPos[i])
            vert = viableVerticalMove(initialPos[i],finalPos[i])
            if initialPos[i] != finalPos[i]:
                moves.append([horiz[0],vert[0],initialPos[i],horiz[1],vert[1]])
            else :
                moves.append([initialPos[i],horiz[0],vert[0],horiz[1],vert[1]])
        best = []
        for i in range(len(initialPos)):
            best.append(moves[i][0])


        if len(best) == len(sort_and_deduplicate(best)):
            print best
            initialPos = list(best)
        else :
            print "WE'RE IN TROUBLE"
            return 666 #NOPE

def duplicates(mylist):
    D = defaultdict(list)
    for i,item in enumerate(mylist):
        D[item].append(i)
    D = {k:v for k,v in D.items() if len(v)>1}
    return D

def checkConflict(best, finalPos, stars):
    starConflicts = []
    conflicts = []
    for i in range(len(best)): #checks for stars
        if best[i] in stars :
            starConflicts.append(i)
    bestTuples = list(tuple(x) for x in best)
    dupes = duplicates(bestTuples)
    for key in dupes : #checks for other conflicts from moves
        indices = dupes[key]
        maxDist = 0
        maxIndex = -1
        for i in indices: # keep the move that is furthest from its destination
            dist = abs(finalPos[i][0] - best[i][0]) + abs(finalPos[i][1] - best[i][1])
            if dist>maxDist:
                maxDist = dist
                maxIndex = i
        dupes[key].remove(maxIndex)
        conflicts = conflicts + dupes[key]

    conflicts = list(set(conflicts))
    return conflicts,starConflicts

def allPositiveMoves(initial,final,size):
    allPos = []

    if initial[0] != final[0]:
        tempPos = list(initial)

        if initial[0] < final[0] and initial[0] < size-1:
            tempPos[0] = tempPos[0] + 1
        elif initial[0] > 0:
            tempPos[0] = tempPos[0] - 1

        allPos.append(tempPos)
    if initial[1] != final[1] :
        tempPos = list(initial)

        if initial[1] < final[1] and initial[1] < size-1:
            tempPos[1] = tempPos[1] + 1
        elif initial[1] > 0:
            tempPos[1] = tempPos[1] - 1

        allPos.append(tempPos)

    return allPos

def pathCost(initialPos, finalPos, stars, size):
    while not checkFinished(initialPos,finalPos):
        best = []
        for i in range(len(initialPos)): #obtain best moves

            tempPos = list(initialPos[i])

            if initialPos[i] != finalPos[i]:
                if initialPos[i][0] != finalPos[i][0]:

                    if initialPos[i][0] < finalPos[i][0] and initialPos[i][0] < size-1:
                        tempPos[0] = tempPos[0] + 1
                    elif initialPos[i][0] > 0:
                        tempPos[0] = tempPos[0] - 1

                else :

                    if initialPos[i][1] < finalPos[i][1] and initialPos[i][1] < size-1:
                        tempPos[1] = tempPos[1] + 1
                    elif initialPos[i][1] > 0:
                        tempPos[1] = tempPos[1] - 1

            best.append(tempPos)
        conflicts,starConflicts = checkConflict(best,finalPos,stars)
        for i in conflicts:
            otherMoves = allPositiveMoves(initialPos[i],finalPos[i],size).remove(best[i])

    #move horizontal, then vertical
    #if conflict : move vertical / horizontal




a = [[0,0],[1,1],[0,0],[1,0]]
b = [[2,2],[2,3],[2,4],[2,5]]

x = list(allPositiveMoves([0,0],[1,1],50))
print x


#CONFLICT => priority to point further away from destination
