import sys
import numpy as np
from collections import defaultdict
from dijkstra import dijkstra

graph = np.zeros((1000,1000),dtype=int).fill(-1)

def parsePath(path):
	pathList = []
	while(path):
		pathList = [path[0]] + pathList
		path = path[1]
	return pathList	


def populateGraph(filename):
	lines = [line.rstrip('\n').split(" ") for line in open(filename)]
	start = int(lines[0][2])
	end = int(lines[1][2])
	lines = lines[3:]

	g = defaultdict(list)
        
	for line in lines:
		graph[int(line[0])][int(line[1])] = 1
		graph[int(line[1])][int(line[0])] = 1
		g[int(line[0])].append((1,int(line[1])))
		g[int(line[1])].append((1,int(line[0])))

	return start,end,g

filename = sys.argv[1]
start,end,graphMat = populateGraph(filename)

dijkstraDistMat = np.zeros((1000,1000),dtype = [('cost','i4'),('nxt','i4')])
dijkstraDistMat['cost'] = -1
dijkstraDistMat['nxt'] = -1
cost,path = dijkstra(graphMat,key1,key2)
path = parsePath(path)

#ignore the stuff below this for now

#print dijkstraDistMat
'''for key1 in graphMat:
	for key2 in graphMat:
		if key1 != key2:
			if dijkstraDistMat[key1][key2]['nxt'] == -1:
				cost,path = dijkstra(graphMat,key1,key2)
				#print len(path)
				path = parsePath(path)
				pathLen = len(path)
				for i in range(pathLen) : 
					idx = pathLen-i
					dijkstraDistMat[key1][idx] = (cost-edge[,path[i]) #fix
					dijkstraDistMat[idx][key1] = (cost,path[len(path)-2])'''
#print dijkstraDistMat[start][end]			
#cost,path = dijkstra(graphMat,start,end)
#print parsePath(path)
#print dijkstraDistMat[508]