#SSP Check
import sys
import numpy as np
edgecolors =  np.zeros((201,201),dtype=int)
edgetime = np.zeros((201,201),dtype=int)
colors = np.zeros((10,2),dtype=int)

def populateEdges(fname):
	#entryname = sys.argv[2]
	#fname = sys.argv[1]

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
			#print line
			line[3] = int(line[3])
		line[0] = int(line[0])
		line[1] = int(line[1])
		line[2] = int(line[2])	
		

	for line in lines:
		#print line[0], line[1]
		if len(line) == 4 :
			edgecolors[line[0]][line[1]] = line[2]
			edgetime[line[0]][line[1]] = line[3]

		else :
			colors[line[0]][0] = line[1]
			colors[line[0]][1] = line[2]

#ACTUAL INTERFACING
def showMoves(entryname):
	#print entryname
	#stats = entryname.readlines()#[line.strip() for line in entryname]
	#print stats
	#startTime = int(stats[0][0])
	#endTime = int(stats[1][0])
	#print line
	#moves = []
	clock = 0
	prevNode = -1
	for line in entryname.splitlines():
		move = line.split()
		#print move
		#line[0] = int(line[0][1:])
		#line[1] = int(line[1][1:])
		#moves.append(line)
		
		startNode = int(move[0][1:])
		finNode = int(move[1][1:])
	
		color = edgecolors[startNode][finNode]
		sumTime = np.sum(colors[color])
		startTime = int(move[2])
		endTime = int(move[3])
		#print startNode,finNode,startTime,endTime
		#print color, sumTime
		moveTime = edgetime[startNode][finNode]
		currEdgeTime = clock%sumTime
		#print currEdgeTime
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

	print "\nTotal Traversal Time = " + str(clock) + "\n"
	sys.exit()

#print moves

'''for i in range(201):
	for j in range(201):
		if edgetime[i][j]!=edgetime[j][i]:
			print str(i) + " " + str(j) + " " + str(edgetime[i][j]) + " " + str(edgetime[j][i])'''
