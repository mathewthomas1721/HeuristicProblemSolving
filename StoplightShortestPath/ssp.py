#SSP Check
import sys
import numpy as np
edgecolors =  np.zeros((201,201),dtype=int)
edgetime = np.zeros((201,201),dtype=int)
colors = np.zeros((10,2),dtype=int)

def populateEdges(fname):

	lines1 = [line.rstrip('\n').split(" ") for line in open(fname)]
	   
	lines = []    
	for line in lines1:
		if line != ['color', 'greentime', 'redtime'] and line != ['', '', '', '', ''] and line !=['node1', 'node2', 'color', 'traversetime'] :
			lines.append(line)
	
	for line in lines :
		line[0] = line[0][1:]
		if len(line) == 4 :
			line[1] = line[1][1:]
			line[2] = line[2][1:]
			line[3] = int(line[3])
		line[0] = int(line[0])
		line[1] = int(line[1])
		line[2] = int(line[2])	
		

	for line in lines:
		if len(line) == 4 :
			edgecolors[line[0]][line[1]] = line[2]
			edgetime[line[0]][line[1]] = line[3]

		else :
			colors[line[0]][0] = line[1]
			colors[line[0]][1] = line[2]

#ACTUAL INTERFACING
def showMoves(entryname,start,finish):
	clock = 0
	prevNode = -1
	firstNode = -1

	for line in entryname.splitlines():
		move = line.split()
		startNode = int(move[0][1:])
		finNode = int(move[1][1:])
		if firstNode == -1 :
			firstNode = startNode
			if firstNode != start :
				print "\nERROR, INCORRECT START NODE " + str(line) + "\n"
				sys.exit()	
	
		color = edgecolors[startNode][finNode]
		sumTime = np.sum(colors[color])
		startTime = int(move[2])
		endTime = int(move[3])
		moveTime = edgetime[startNode][finNode]
		currEdgeTime = clock%sumTime
		if startNode == prevNode or prevNode == -1:
			if moveTime != 0:
				if moveTime==(endTime-startTime) :
					if ((currEdgeTime + moveTime) % sumTime) <= colors[color][0]:
						clock = endTime
						prevNode = finNode
						print line
					else :
						print "\nERROR, ILLEGAL TRAVERSAL, OUTSIDE OF GREENTIME " + str(line) + "\n"
						sys.exit()	
				else :
					print "\nERROR, MOVE TIMES DO NOT MATCH " + str(line) + " " + str(moveTime) + "\n"
					sys.exit()
			else :
				print "\nERROR, EDGE DOES NOT EXIST " + str(line) + "\n"
				sys.exit()
		else:
			print "\nERROR, TRAVERSAL NOT CONTINUOUS " + str(line) + "\n"
			sys.exit()
	
	lastNode = finNode
	if(lastNode!=finish):
		print "\nERROR, INCORRECT END NODE " + str(line) + "\n"
		sys.exit()	
	print "\nPath from " + str(firstNode) + " to " + str(lastNode) + "\n"
	print "\nTotal Traversal Time = " + str(clock) + "\n"
	sys.exit()

