from Compat import *


n, m, k = map(int, input().split())
g = [[a for a in map(int, input().split())] for i in range(k)]

s = Solver(n, m, k)

s.parse_compats(g)
CSolver = s.set_search()
s.generate_output(CSolver)
