import numpy as np 
import sys
from client import Client

#The initial number of stones is guaranteed to be less than 1000, so we can create the table of game states up to 1000 stones
num_stones = 1000
#Players start with 4 resets
num_resets = 4

"""
Initialize 5-dimensional array of every possible game state:
	1 - 1000 stones remaining
	1 - 45 current_max (45 is the highest the current_max can go with 1000 initial stones)
	0 - 4 resets left for player 1
	0 - 4 resets left for player 2
	reset either on or off
"""
bs_moves = np.zeros((num_stones,45, num_resets + 1, num_resets + 1,2), dtype=np.int)

"""
	Use dynamic programming to fill out a loaction in the move table for the game state with NO RESET ACTIVE
	and a game state given by the inputs:
		stones: Number of remaining stones
		curr_max: The current maximum number of stones that a player can take.
		num_rs1: The number of remaining resets the player whose turn it is has.
		num_rs2: THe number of remaining resets that player's opponent has.
	Fills location with one of the following:
		0: This means that this is a losing position. There are no moves that can lead to a winning position assuming 
			the opponent doesn't make a mistake. In this case your move doesn't really matter.
		positive integer i: Take i stones and DON'T use a reset to keep player in a winning position.
		negative integer -i: Take i stones and use a reset.
"""
def populate(stones, curr_max, num_rs1, num_rs2):

	#Whole array is initialized to 0s, so if we don't find a winning move, the entry will remain 0, signifying a losing position
	# The -1's and -3's in all of the array lookups are to offset the fact that we want stones to start at 1 and 
	# current max to start at 3, but indices are 0-based

	#check moves from 1 to curr_max - 1
	for i in range(1, curr_max):
		# if the outcome of a move is a LOSING position for the opponent (a 0), write that move in the spot and return
		# move with no reset
		if (bs_moves[stones - i - 1, curr_max - 3, num_rs2, num_rs1, 0] == 0):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 0] = i
			return
		#move with reset. Notice that the number of resets swap when we look this up because 
		#We are looking to see if the result is a losing move for the OTHER player. Our num_rs goes down by 1
		if ((num_rs1 > 0) and (bs_moves[stones - i - 1, curr_max - 3, num_rs2, num_rs1 - 1, 1] == 0)):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 0] = -1 * i #use reset
			return
	#Moves taking current max stones. This is separate because the resulting location has an incremented curr_max
	if (bs_moves[stones - curr_max - 1, curr_max - 2, num_rs2, num_rs1,0] == 0):
		bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 0] = curr_max
		return
	if ((num_rs1 > 0) and (bs_moves[stones - curr_max - 1, curr_max - 2, num_rs2, num_rs1 - 1,1] == 0)):
		bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 0] = -1 * curr_max #use reset
		return

"""
	Use dynamic programming to fill out a loaction in the move table for the game state with RESET ACTIVE
	Same exact inputs and results as the previous function, but we only check between 1 and 3 stones
	"""	
def populate_reset_on(stones, curr_max, num_rs1, num_rs2):
	bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2,1] = 0
	for i in range (1,4):
		changemax = 0 #This bit of code accounts for the posibility that someone uses a reset when curr_max is still 3, 
		if (i == curr_max): #and then player takes 3 stones.
			changemax = 1
		#Don't use reset
		if (bs_moves[stones - i - 1, curr_max - 3 + changemax, num_rs2, num_rs1, 0] == 0):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 1] = i
			return
		#use reset
		if ((num_rs1 > 0) and (bs_moves[stones - i - 1, curr_max - 3 + changemax, num_rs2, num_rs1 - 1, 1] == 0)):
			bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, 1] = -1 * i #use reset
			return


"""
	Fill in the 5d array of game states with the correct moves. 
	We fill in some values explicitly: When the number of stones remaining is less than or 
	equal to the number of stones the player is permitted to take that turn, the correct winning move is to take all the stones.
	For all opther game states, we call a function above that will fill that game state by looking at previously filled states
	to evaluate the outcome of all legal moves from that position.
"""		
def fill_mat():
	for i in range(num_stones): # i is the number of stones left - 1
		for j in range(42): #j is the current_max - 3
			for k in range(num_resets + 1): #k is the current players number of resets left
				for l in range(num_resets + 1): #l is the opponents number of resets left
					stones = i + 1
					curr_max = j + 3
					if (stones <= curr_max): #If we can take all the stones, do that
						bs_moves[i, j, k, l,0] = stones
						if (stones <= 3):
							bs_moves[i, j, k, l,1] = stones
						else:
							populate_reset_on(stones, curr_max, k, l) # 
					elif (i + 1 <= 1003 - ((j+3)*(j+2)/ 2)): #fill state only if it is possible to get curr_max that high 
															 #starting from 1000 stones. This eliminates part of the array and 
															 #improves performance
						populate(stones, curr_max, k, l) #fill no-reset side
						populate_reset_on(stones, curr_max, k, l) #fill reset side

"""
Function to get a move given a game state
Input: (number of stones remaining, the current max, number of resets left for player 1, number of resets left for player 2, rs=1 for reset on, 0 for no reset)
"""
def get_move(stones, curr_max, num_rs1, num_rs2, rs):
	print(stones, curr_max, num_rs1, num_rs2, rs)
	mv = int(bs_moves[stones - 1, curr_max - 3, num_rs1, num_rs2, rs]) #look up game state in the array
	if (mv == 0): #if we are in a losing position, choose a random legal move that does not use a reset
		if (rs == 1):
			return (np.random.choice(3) + 1, 0)
		return (np.random.choice(curr_max) + 1, 0)
	if (mv < 0): #If entry was negative, take -mv stones and use reset
		return (-1 * mv, 1)
	return (mv, 0) #otherwise take the designated number of stones and don't use a reset

"""Get move from standard input. Used in testing"""
def get_human_move():
	mv = input("Enter Move: ")
	move = mv.split()
	if (len(move) == 1):
		move.append(0)
	return (int(move[0]), int(move[1]))


"""Fuction for printing parts of the move table. Used in debugging"""
def print_mat():
	for i in range(100):
		s = str(int((bs_moves[i, 0, num_resets, num_resets , 0])))
		print(s)
#comment PAUL

"""Class managing the execution on a game of Expanding Nim over the Server"""
class Server_Game:
	#Create a client object to connect to the server at the given ip address and port
	#turnx = 0 for the first player
	#turnx = 1 for the second player
	def __init__(self,ip, port,turnx):
		#server_addr = ["172.16.183.135","9000"]

		self.client = Client('BabySnake', (turnx == 0), (ip,port))
		self.stones = self.client.init_stones #Have the client get the number of initial stones from the server
		#all other gameplay variables can be initialized to known values
		self.num_rs1 = 4
		self.num_rs2 = 4
		self.curr_max = 3
		self.isReset = 0
		self.turn = turnx
		self.fin = False

	def make_move(self):
		#get move based on current game state
		mv = get_move(self.stones, self.curr_max, self.num_rs1, self.num_rs2, self.isReset)
		print(mv)
		status = {}
		#increment current_max if necessary
		if (mv[0] == self.curr_max):
			self.curr_max += 1
		#Make move with reset and update resets left
		if (mv[1] == 1):
			status = self.client.make_move(int(mv[0]), True)
			self.num_rs1 -= 1
		#Make move without using reset
		else:
			status = self.client.make_move(int(mv[0]), False)
		self.turn = 1 # give turn to other player
		self.fin = status['finished'] 

	def get_move(self):
		status = self.client.receive_move() #get move from server
		#update game state by accessing status dictionary
		self.fin = status['finished'] 
		self.stones = status['stones_left']
		if (status['stones_removed'] == self.curr_max):
			self.curr_max += 1;
		if (status['reset_used']):
			self.isReset = 1
			self.num_rs2 -= 1
		else:
			self.isReset = 0
		self.turn = 0 #give control back to player

	#Loop to play a game over the server
	def play(self):
			while(not self.fin): #check if game is over after each player's move
				if (self.turn == 0):
					self.make_move()
				else:
					self.get_move()

	"""Class to test program against a human player. Not used in competition"""
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

#Call to fill the move table
fill_mat()


addr = sys.argv[1].split(':')
ip = addr[0] # get IP from command line
port = int(addr[1]) #get port from command line
print (ip, port) #
turnx = int(sys.argv[2]) #get command line argument specifying whether we are the first or second player

#Create a new server game and play
game = Server_Game(ip, port,turnx)
game.play()

"""while (1):
	play_human()
"""

