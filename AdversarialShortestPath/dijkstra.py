from collections import defaultdict
from heapq import *

def dijkstra(g, f, t):
	
	q, seen = [(0,f,())], set()
	while q:
		(cost,v1,path) = heappop(q)
		if v1 not in seen:
			seen.add(v1)
			path = (v1, path)
			
			if v1 == t: 
				return cost, path
				
			for c, v2 in g.get(v1, ()):
				if v2 not in seen:
					heappush(q, (cost+c, v2, path))

	return float("inf")

