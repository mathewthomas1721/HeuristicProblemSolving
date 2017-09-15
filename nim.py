import numpy as np 

num_stones = 1000
num_resets = 4

bs_moves = np.zeros((num_stones,45, num_resets + 1, num_resets + 1,2))

def populate(stones, curr_max, num_rs1, num_rs2):

	bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2,0] = 0

	bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2,1] = 0
	#If not in reset
	for i in range(1, curr_max):
		if (bs_moves[stones - i - 1, curr_max - 3, num_rs2, num_rs1, 0] == 0):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 0] = i
		if ((num_rs1 > 0) and (bs_moves[stones - i - 1, curr_max - 3, num_rs2, num_rs1 - 1, 1] == 0)):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 0] = -1 * i #use reset
	if (curr_max < 45):
		if (bs_moves[stones - curr_max - 1, curr_max - 2, num_rs2, num_rs1,0] == 0):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 0] = curr_max
		if ((curr_max < 45) and (bs_moves[stones - curr_max - 1, curr_max - 2, num_rs2, num_rs1 - 1,1] == 0)):
				bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 0] = -1 * curr_max #use reset
	#If in reset
	for i in range (1,4):
		if (bs_moves[stones - i - 1, curr_max - 3, num_rs2, num_rs1, 0] == 0):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 1] = i
		if ((num_rs1 > 0) and (bs_moves[stones - i - 1, curr_max - 3, num_rs2, num_rs1 - 1, 1] == 0)):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 1] = -1 * i #use reset
		
def fill_mat():
	for i in range(num_stones):
		for j in range(42):
			for k in range(num_resets + 1):
				for l in range(num_resets + 1):
					stones = i + 1
					curr_max = j + 3
					if (stones <= curr_max):
						bs_moves[i, j, k, l,0] = stones
					if (stones <= 3):
						bs_moves[i, j, k, l,1] = stones
					elif ((num_stones - i)):
						populate(stones, curr_max, k, l)

def get_move(stones, curr_max, num_rs1, num_rs2, rs):
	mv = bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, rs]
	if (mv == 0):
		if (rs == 1):
			return (np.random.choice(3) + 1, 0)
		return (np.random.choice(curr_max) + 1, 0)
	if (mv < 0):
		return (-1 * mv, 1)
	return (mv, 0)

def get_human_move():
	mv = input("Enter Move: ")
	move = mv.split()
	if (len(move) == 1):
		move.append(0)
	return (int(move[0]), int(move[1]))


def print_mat():
	for i in range(num_stones):
		s = str(int((bs_moves[i, 0, num_resets, num_resets , 0])))
		print(s)
#comment PAUL


class Game:
	def __init__(self):
		self.stones = np.random.choice(25)
		self.num_rs1 = 4
		self.num_rs2 = 4
		self.curr_max = 3
		self.turn = np.random.choice(2)
		self.isReset = 0

	def __str__(self):
		s = "Stones Remaining: " + str(self.stones) + "\n"
		return s

	def human_prompt(self):
		s = "The current maximum is " + str(self.curr_max) + " stones. "
		s += "You have " + str(self.num_rs1) + " resets left. "
		s += "The computer has " + str(self.num_rs2) + " resets left.\n"
		if (self.isReset == 1):
			s += "Reset active (Take at most 3 stones.)\n"
		return s

	def play(self):
		while (self.stones > 0):
			print(self)
			if (self.turn == 0):
				print(self.human_prompt())
				mv = get_human_move()
				self.stones -= mv[0]
				if (mv[0] == self.curr_max and self.isReset == 0):
					self.curr_max += 1
				self.num_rs1 -= mv[1]
				self.isReset = mv[1]
				self.turn = 1
			elif (self.turn == 1):
				mv = get_move(self.stones, self.curr_max, self.num_rs2, self.num_rs1, self.isReset)
				self.stones -= mv[0]
				if (mv[0] == self.curr_max and self.isReset == 0):
					self.curr_max += 1
				self.num_rs2 -= mv[1]
				self.isReset = mv[1]
				self.turn = 0
				output = "Computer removes " + str(mv[0]) + " stones and "
				if (self.isReset == 1):
					output += "uses"
				else:
					output += "does not use"
				output += " reset."
				print(output)
		if (self.turn == 0):
			print("Computer wins")
		else:
			print("Human wins")


def play_human():
	game = Game() 
	game.play()

fill_mat()
"""while (1):
	play_human()"""


<<<<<<< HEAD
=======
for i in xrange(1000):
	s = ""
	for j in xrange(42):
		s += str(int((bs_moves[i, j]))) + " "
	print s
#comment PAUL MATT
>>>>>>> 1205b7a2aaac55eb5ac84fa6ae12217c17b9944f
