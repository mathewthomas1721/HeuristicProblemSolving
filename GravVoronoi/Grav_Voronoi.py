import numpy as np
from voronoi_client import Client

NUM_COLORS = 2
BOARD_SIZE = 1000



def dist(x1, y1, x2, y2):
	return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def attract(x1, y1, x2, y2):
	d = dist(x1, y1, x2, y2)
	if d == 0:
		return float('inf')
	else:
		return 1.0 / (d ** 2)

def compute_color(pos_x, pos_y, board):
	max_attract = 0
	max_color = 0
	for c in range(NUM_COLORS):
		if board[pos_y, pos_x, c] > max_attract:
			max_attract = board[pos_y, pos_x, c]
			max_color = c
	return c

