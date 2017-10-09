import sys
import numpy as np
from collections import defaultdict
from dijkstra import *

graph = np.zeros((1000,1000))
graph.fill(-1)

def parsePath(node, Dpaths):
	pathList = [node]
	cost = -1
	curr = node
	nxt = node
	cost, nxt = Dpaths[node]
	while not (nxt == -1):
		pathList.append(nxt)
		node = nxt
		nxt = Dpaths[node][1]
	return pathList, cost

def parsePathOld(path):
	pathList = []
	while(path):
		pathList.append(path[0])
		path = path[1]
	return pathList	

def getCost(path):
	cost = 0
	while path[1]:
		v1 =  path[0]
		path = path[1]
		v2 = path[0]
		cost += graph[v1,v2]
	return cost


def populateGraph(filename):
	lines = [line.rstrip('\n').split(" ") for line in open(filename)]
	start = int(lines[0][2])
	end = int(lines[1][2])
	lines = lines[3:]

	g = defaultdict(list)
    #g_weights = defaultdict(list)
	for line in lines:
		graph[float(line[0]), float(line[1])] = 1
		graph[float(line[1]), float(line[0])] = 1
		g[int(line[0])].append((1,int(line[1])))
		g[int(line[1])].append((1,int(line[0])))
		#h[int(line[0])].append((1,int(line[1])))
		#h[int(line[1])].append((1,int(line[0])))

	return start,end,g, #h

def increase_edge(v1, v2, Dpaths):
	dist1 = Dpaths[v1][0]
	dist2 = Dpaths[v2][0]
	dist = min(dist1, dist2)
	if dist < 0:
		dist = 0
	factor = 1.0 + np.sqrt(dist)
	graph[v1][v2] *= factor
	graph[v2][v1] *= factor
	return factor


def get_move(Dpaths, graphMat, start, end):
	path, dist = parsePath(start, Dpaths)
	cost = float('inf')
	for p in AllPathsN(graphMat, end, start, dist, Dpaths):
		c = getCost(p)
		if (c < cost):
			path = parsePathOld(p)
			cost = c
	return path[1]

def get_A_move(Dpaths, graphMat, start, end):
	path, distance = parsePath(start, Dpaths)
	cost = float('inf')
	for p in AllPathsN(graphMat, end, start, distance, Dpaths):
		c = getCost(p)
		if (c < cost):
			path = parsePathOld(p)
			cost = c
	print path
	max_penalty = -1
	move = (-1,-1)
	for i in range(1,len(path)):
		v1 = path[i - 1]
		v2 = path[i]
		dist1 = Dpaths[v1][0]
		dist2 = Dpaths[v2][0]
		dist = min(dist1, dist2)
		if (dist < 0 ):
			dist = 0
		factor = 1.0 + np.sqrt(dist)
		penalty = graph[v1][v2] * factor ** (distance - dist) - graph[v1][v2]
		if penalty > max_penalty:
			max_penalty = penalty
			move = (v1,v2)
	return move


def game(filename):
	start,end,graphMat = populateGraph(filename)
	Dpaths = dijkstra(graphMat,end)
	current_v = start
	total_cost = 0
	for p in AllPathsN(graphMat, end, start, Dpaths[start][0], Dpaths):
		print parsePathOld(p)
	move = get_move(Dpaths, graphMat, start, end)
	total_cost += graph[current_v][move]
	print "Player moves from vertex " + str(current_v) + " to vertex " + str(move) + " and pays "  + str(graph[current_v][move]) + ". Total cost: " + str(total_cost) + "\n"
	current_v = move
	while (current_v != end):
		a_move = get_A_move(Dpaths, graphMat, current_v, end)
		fac = increase_edge(a_move[0], a_move[1], Dpaths)
		print "Adversary increases edge " + str(a_move) + " by a factor of " + str(fac) + ". New Cost: " + str(graph[a_move[0], a_move[1]]) + "\n"
		move = get_move(Dpaths, graphMat, current_v, end)
		total_cost += graph[current_v][move]
		print "Player moves from vertex " + str(current_v) + " to vertex " + str(move) + " and pays "  + str(graph[current_v][move]) + ". Total cost: " + str(total_cost) + "\n"
		current_v = move





filename = sys.argv[1]
game(filename)
"""start,end,graphMat = populateGraph(filename)


dijkstraDistMat = np.zeros((1000,1000),dtype = [('cost','i4'),('nxt','i4')])
dijkstraDistMat['cost'] = -1
dijkstraDistMat['nxt'] = -1
Dpaths = dijkstra(graphMat,end)
path, cost = parsePath(start, Dpaths)
print path, cost
for p in AllPathsN(graphMat, end, start, cost, Dpaths):
	print str(parsePathOld(p)) + " cost: " + str(getCost(p))  + "\n"

	"""

