def checkFinished(curr,final):
    for i in range(len(curr)):
        if curr[i] != final[i]:
            return False
    return True

def pathCost(initialPos, finalPos, stars):
    while not checkFinished(initialPos,finalPos):
        for i in range(len(initialPos)):
