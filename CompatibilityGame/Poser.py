from Compat import *


n, m, k = map(int, input().split())



p = Eviler_Poser(n, m, k)
p.generate_compats()
p.generate_output()
