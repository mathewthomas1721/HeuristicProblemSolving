import numpy as np 
import sys
from client import Client

num_stones = 1000
num_resets = 4

bs_moves = np.zeros((num_stones,45, num_resets + 1, num_resets + 1,2), dtype=np.int)

def populate(stones, curr_max, num_rs1, num_rs2):

	bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2,0] = 0

	#If not in reset
	for i in range(1, curr_max):
		if (bs_moves[stones - i - 1, curr_max - 3, num_rs2, num_rs1, 0] == 0):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 0] = i
			return
		if ((num_rs1 > 0) and (bs_moves[stones - i - 1, curr_max - 3, num_rs2, num_rs1 - 1, 1] == 0)):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 0] = -1 * i #use reset
			return
	if (curr_max < 45):
		if (bs_moves[stones - curr_max - 1, curr_max - 2, num_rs2, num_rs1,0] == 0):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 0] = curr_max
			return
		if ((num_rs1 > 0) and (bs_moves[stones - curr_max - 1, curr_max - 2, num_rs2, num_rs1 - 1,1] == 0)):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 0] = -1 * curr_max #use reset
			return


def populate_reset_on(stones, curr_max, num_rs1, num_rs2):
	bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2,1] = 0
	for i in range (1,4):
		changemax = 0
		if (i == curr_max):
			changemax = 1
		if (bs_moves[stones - i - 1, curr_max - 3 + changemax, num_rs2, num_rs1, 0] == 0):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 1] = i
			return
		if ((num_rs1 > 0) and (bs_moves[stones - i - 1, curr_max - 3 + changemax, num_rs2, num_rs1 - 1, 1] == 0)):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 1] = -1 * i #use reset
			return


		
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
						else:
							populate_reset_on(stones, curr_max, k, l)
					else:
						populate(stones, curr_max, k, l)
						populate_reset_on(stones, curr_max, k, l)

def get_move(stones, curr_max, num_rs1, num_rs2, rs):
	print(stones, curr_max, num_rs1, num_rs2, rs)
	mv = int(bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, rs])
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
	for i in range(100):
		s = str(int((bs_moves[i, 0, num_resets, num_resets , 0])))
		print(s)
#comment PAUL

class Server_Game:
	def __init__(self,turnx):
		#server_addr = ["172.16.183.135","9000"]

		self.client = Client('BabySnake', (turnx == 0), ('192.168.1.158',9000))
		self.stones = self.client.init_stones
		self.num_rs1 = 4
		self.num_rs2 = 4
		self.curr_max = 3
		self.isReset = 0
		self.turn = turnx
		self.fin = False

	def make_move(self):

		mv = get_move(self.stones, self.curr_max, self.num_rs1, self.num_rs2, self.isReset)
		print(mv)
		if (mv[0] == self.curr_max):
			self.curr_max += 1
		if (mv[1] == 1):
			self.client.make_move(int(mv[0]), True)
			self.num_rs1 -= 1
		else:
			self.client.make_move(int(mv[0]), False)
		self.turn = 1

	def get_move(self):
		status = self.client.receive_move()
		self.fin = status['finished']
		self.stones = status['stones_left']
		if (status['stones_removed'] == self.curr_max):
			self.curr_max += 1;
		if (status['reset_used']):
			self.isReset = 1
			self.num_rs2 -= 1
		else:
			self.isReset = 0
		self.turn = 0

	def play(self):
			while(not self.fin):
				if (self.turn == 0):
					self.make_move()
				else:
					self.get_move()

class Human_Game:
	def __init__(self):
		self.stones = np.random.choice(50) + 1
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
				print(mv)
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
	game = Human_Game() 
	game.play()

fill_mat()


turnx = int(sys.argv[1])
print(turnx)
game = Server_Game(turnx)
game.play()

"""while (1):
	play_human()
"""

