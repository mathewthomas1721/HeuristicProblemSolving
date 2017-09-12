import numpy as np
bSnakeMat = np.full([1000, 45], 0)
for i in xrange(1000):
	for j in xrange(45):
		if i<=j:
			bSnakeMat = i
