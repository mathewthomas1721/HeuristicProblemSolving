from collections import defaultdict
from heapq import *
import numpy as np

def dijkstra(g, f):
	dijkstraPathMap = np.zeros(1000,dtype = [('cost','i4'),('nxt','i4')])	
	dijkstraPathMap.fill(-1)
	q, seen = [(0,f,())], set()
	while q:
		(cost,v1,path) = heappop(q)
		if v1 not in seen:
			seen.add(v1)
			if (not path == ()):
				dijkstraPathMap[v1] = (cost, path[0])
			path = (v1, path)
			"""
			if v1 == t: 
				return cost, path
				"""
			for c, v2 in g.get(v1, ()):
				if v2 not in seen:
					heappush(q, (cost+c, v2, path))

	return dijkstraPathMap


def AllPathsN(g, f, t, N, dists):
	paths = []
	q, seen = [(0,f,())], set()
	while q:
		(cost,v1,path) = heappop(q)
		if (v1 not in seen) or cost == dists[v1][0]:
			seen.add(v1)
			
			path = (v1, path)
			
			if v1 == t: 
				paths.append(path)
				
			for c, v2 in g.get(v1, ()):
				newC = cost + c
				if (v2 not in seen or newC == dists[v2][0]) and newC <= N :
					heappush(q, (newC, v2, path))

	return paths