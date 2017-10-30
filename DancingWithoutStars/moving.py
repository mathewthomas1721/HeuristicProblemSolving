def checkFinished(curr,final):
    for i in range(len(curr)):
        if curr[i] != final[i]:
            return False
    return True

def pathCost(initialPos, finalPos, stars):
    cost = 0
    skip = []
    while not checkFinished(initialPos,finalPos):
        print skip
        for i in range(len(initialPos)):
            print initialPos[i]
            if initialPos[i] != finalPos[i]:
                if initialPos[i][0] != finalPos[i][0] :
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

                            initialPos[i] = test
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
                        initialPos[i] = test
                    else :
                        test = initialPos[i]
                        test[1] = test[1] - 1
                        if test in stars:
                            test[0] = test[0] + 1
                            #test[1] = test[1] + 1
                            skip.append(i)
                        initialPos[i] = test
        cost = cost + 1

    return cost
a = [[0,0]]
b = [[-5,7]]
print pathCost(a,b,[[-5,4]])
