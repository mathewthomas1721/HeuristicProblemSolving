import sys
import numpy as np
from collections import defaultdict
from dijkstra import *

graph = np.zeros((1000,1000))
graph.fill(-1)

def updateGraph (v1,v2,val):
	graph[v1][v2] = val

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


def populateGraph(game):
	
	adjlist = game['graph']
	start = int(game['start_node'])
	end = int(game['end_node'])
	g = defaultdict(list)
	for key in adjlist:
		for node in adjlist[key]:
			graph[int(key),int(node)] = 1
			g[int(key)].append((1,int(node)))
			
	return start,end,g

def edge_in_all(paths, cost, v1, v2):
	for p in paths:
		parsed = parsePathOld(p)
		if getCost(p) <= cost + 1:
			if not (v1 in parsed and v2 in parsed):
				return False
	return True

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
	for p in AllPathsN(graphMat, end, start, dist + 1, Dpaths):
		c = getCost(p)
		if (c < cost):
			path = parsePathOld(p)
			cost = c

	return (path[0], path[1])

def max_Penalty(Dpaths, graphMat, start, end):
	path, distance = parsePath(start, Dpaths)
	cost = float('inf')
	for p in AllPathsN(graphMat, end, start, distance, Dpaths):
		c = getCost(p)
		if (c < cost):
			path = parsePathOld(p)
			cost = c
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
		penalty = graph[v1][v2] * factor ** (distance - dist) - graph[v1][v2] + max_Penalty(Dpaths, graphMat, v2, end)
		if penalty > max_penalty:
			max_penalty = penalty
			move = (v1,v2)
	if max_penalty < 0:
		return 0
	return max_penalty

def get_A_move(Dpaths, graphMat, start, end):
	path, distance = parsePath(start, Dpaths)
	cost = float('inf')
	paths = AllPathsN(graphMat, end, start, distance, Dpaths)
	for p in paths:
		c = getCost(p)
		if (c < cost):
			path = parsePathOld(p)
			cost = c
	#print path
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
		if (edge_in_all(paths, cost, v1, v2)):
			penalty = penalty * 5
		penalty += max_Penalty(Dpaths, graphMat, v2, end)
		#print "(" + str(v1) + ", " + str(v2) + "): " + str(penalty)
		if penalty > max_penalty:
			max_penalty = penalty
			move = (v1,v2)
	increase_edge(move[0], move[1], Dpaths)	
	return move


def game(filename):
	start,end,graphMat = populateGraph(filename)
	Dpaths = dijkstra(graphMat,end)
	current_v = start
	total_cost = 0
	for p in AllPathsN(graphMat, end, start, Dpaths[start][0], Dpaths):
		print parsePathOld(p)
	move = get_move(Dpaths, graphMat, start, end)[1]
	total_cost += graph[current_v][move]
	print "Player moves from vertex " + str(current_v) + " to vertex " + str(move) + " and pays "  + str(graph[current_v][move]) + ". Total cost: " + str(total_cost) + "\n"
	current_v = move
	while (current_v != end):
		a_move = get_A_move(Dpaths, graphMat, current_v, end)
		fac = increase_edge(a_move[0], a_move[1], Dpaths)
		print "Adversary increases edge " + str(a_move) + " by a factor of " + str(fac) + ". New Cost: " + str(graph[a_move[0], a_move[1]]) + "\n"
		move = get_move(Dpaths, graphMat, current_v, end)[1]
		total_cost += graph[current_v][move]
		print "Player moves from vertex " + str(current_v) + " to vertex " + str(move) + " and pays "  + str(graph[current_v][move]) + ". Total cost: " + str(total_cost) + "\n"
		current_v = move

