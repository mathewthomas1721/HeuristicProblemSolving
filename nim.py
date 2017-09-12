import numpy as np 

bs_mat = np.zeros((1000,45))
bs_moves = np.zeros((1000,45))

def populate(stones, curr_max):
	bs_mat[stones - 1, curr_max - 3] = -1
	bs_moves[stones - 1, curr_max - 3] = 0
	for i in xrange(1, curr_max):
		if (bs_mat[stones - i - 1, curr_max - 3] == -1):
			bs_mat[stones - 1, curr_max - 3] = 1
			bs_moves[stones - 1, curr_max - 3] = i
	if (curr_max < 45):
		if (bs_mat[stones - curr_max - 1, curr_max - 2] == -1):
			bs_mat[stones - 1, curr_max - 3] = 1
			bs_moves[stones - 1, curr_max - 3] = curr_max


for i in xrange(1000):
	for j in xrange(42):
		stones = i + 1
		curr_max = j + 3
		if (stones <= curr_max):
			bs_mat[i, j] = 1
			bs_moves[i, j] = stones
		else:
			populate(stones, curr_max)





for i in xrange(1000):
	s = ""
	for j in xrange(42):
		s += str(int((bs_moves[i, j]))) + " "
	print s
#comment PAUL MATT
