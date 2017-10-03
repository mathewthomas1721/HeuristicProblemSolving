from board import Board
import numpy as np
import copy
LEVEL = 1
# How do we choose an optimum move?
#
# What is it dependent on? 
#
# 1. Remaining Spaces
# 2. Whether it's placing, or removing
# 3. What weights the player has
# 4. What weights the opponent has
#
# How does it vary? What's our strategy? 
# What's our goal?
#
# Goal - don't tip the board
# How do we do that? 
# Less likely to tip if - 
# 1. We place weights on the points closer to the supports
# 2. We place lighter weights further away from the supports
#
# So, our strategy  - Place as many heavy weights as possible towards the middle
# and use smaller weights as we go out
def score(boardCurr, player): # Defines a score for each state
	score = 0.0
	allmoves = 0
	if player == 1:
		weights = boardCurr.myBlocks
	else :
		weights = boardCurr.oppBlocks	
	#size = len(boardCurr.board)/2
	for weight in weights:
		if weight != 0:
			for pos in range(-30,31):
				if boardCurr.lookup(pos) == 0 :
					boardCurr.place(player, weight, pos)
					if boardCurr.tip():
						#print "TIP"
						score = score + 1
					#else : 
						#score = score -1
					allmoves = allmoves + 1		
					boardCurr.remove(player,weight,pos)
	#if score > 0:				
	#	print score/allmoves
	#if allmoves = 0 : 
	#	return 1.5 #FAILURE				
	return score/allmoves

		
	
def childStatesAdd(boardCurr, player): # Populates a list containing all valid moves FOR ADDING WEIGHTS - OPTIMIZE WITH JUST MOVES
	children = []

	if player == 0:
		weights = list(boardCurr.myBlocks)
	else :
		weights = list(boardCurr.oppBlocks)
	
	for weight in weights : 
		if weight != 0:
			for pos in range(-30,31):
				if boardCurr.lookup(pos) == 0 :
					
					boardCurr.place(player, weight, pos)
		
					if not boardCurr.tip():

						x = copy.deepcopy(boardCurr)
						children.append(x)

					boardCurr.remove(player, weight, pos)
	children.reverse()		
	return children	
# alpha -> Best already explored option along path to the root for maximizer
# beta -> Best already explored option along path to the root for minimizer
def childStatesRemove(boardCurr,player): # Populates a list containing all valid moves FOR ADDING WEIGHTS - OPTIMIZE WITH JUST MOVES
	children = []
	
	for pos in range(-30,31):
		weight = boardCurr.lookup(pos)
		if weight != 0 :
			
			boardCurr.remove(player, weight, pos)

			if not boardCurr.tip():

				x = copy.deepcopy(boardCurr)
				children.append(x)

			boardCurr.place(player, weight, pos)	

		
	return children	

def alpha_beta_search(boardCurr,addrem):
    #print board
    alpha = -float("inf")
    beta = float("inf")
    print score(boardCurr,0)
    bscore, bestBoard = alpha_beta_max_value(boardCurr,alpha,beta,0,0,addrem)
    print bscore
    #print bestBoard.board
    return bestBoard

#The Alpha Beta Max Value
def alpha_beta_max_value(boardCurr,alpha,beta,level,player,addrem):

    if(level >= LEVEL):
    	
        return score(boardCurr, player), boardCurr

    v = -float("inf")
    if addrem == 0:
    	a = childStatesAdd(boardCurr, player)
    else :
    	a = childStatesRemove(boardCurr, player)	

    newboard = []

    if player == 0: 
    	p1 = 1
    else:
    	p1 = 0	
    
    for i in a:
    	#if not np.array_equal(i.board,boardCurr.board):
    	#	print i.board
        val, c = alpha_beta_min_value(i, alpha, beta, level + 1, p1, addrem)

        v = max( v, val)
        #print v
        if( v > beta ):
            return v, boardCurr
        alpha = max( alpha, v )
        newboard = i

    return v, newboard

#The Alpha Beta Min Value
def alpha_beta_min_value(boardCurr,alpha,beta,level,player,addrem):

    if(1):
    	#print "LEVEL REACHED MIN"
        return score(boardCurr, player), boardCurr

    v = float("inf")
    #print "CALL FROM MIN"
    if addrem == 0:
    	a = childStatesAdd(boardCurr, player)
    else :
    	a = childStatesRemove(boardCurr, player)

    newboard = []

    if player == 0: 
    	p1 = 1
    else:
    	p1 = 0

    for j in a:
    	#if not np.array_equal(j.board,boardCurr.board):
    	#	print j.board
        val, c = alpha_beta_max_value(j,alpha,beta,level + 1, p1, addrem)

        v = min( v, val)

        if(v < alpha):
            return v, boardCurr
        beta = min( beta, v )
        newboard = j

	return v, newboard 
			
#b = Board(25)
#weights = list(xrange(1,26))

# HAVE TO FIGURE OUT THE WEIGHTS THAT THE OTHER PLAYER HAS - DONE ALREADY

#x = alpha_beta_search(b).board
#print x
#for i in range(len(x)):
#	if x[i] > 0:
#		print i
#print weights
#listof = childStatesAdd(b,weights)
#for item in listof:
#	print item[1]
