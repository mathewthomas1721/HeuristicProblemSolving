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
	stats = [line.rstrip('\n').split(" ") for line in open(entryname)]
	startTime = int(stats[0][0])
	endTime = int(stats[1][0])
	moves = []
	for line in stats:
		if len(line)>1:
			line[0] = int(line[0][1:])
			line[1] = int(line[1][1:])
			moves.append(line)
	clock = 0;
	for move in moves:
		color = edgecolors[move[0]][move[1]]
		sumTime = np.sum(colors[color])
		#print color, sumTime
		moveTime = edgetime[move[0]][move[1]]
		currEdgeTime = clock%sumTime
		if currEdgeTime + moveTime <=colors[color][0]:
			clock = clock + moveTime
		else :
			print "ERROR, ILLEGAL TRAVERSAL" + str(move)
	print "Total Traversal Time = " + str(clock)	

#print moves

'''for i in range(201):
	for j in range(201):
		if edgetime[i][j]!=edgetime[j][i]:
			print str(i) + " " + str(j) + " " + str(edgetime[i][j]) + " " + str(edgetime[j][i])'''
