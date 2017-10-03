import numpy as np

SUPPORTA = -3
SUPPORTB = -1
BOARDSIZE = 30
BOARDWEIGHT = 3


class Board():

	def __init__(self, k):
		self.k = k
		self.board = np.zeros(2*BOARDSIZE +1)
		self.boardSet(-4, 3)
		self.myBlocks = list(xrange(1,k+1))
		self.oppBlocks = list(xrange(1,k+1))
		self.calcTorques()

	def lookup(self, boardpos):
		#print boardpos, BOARDSIZE
		return self.board[boardpos + BOARDSIZE]

	def boardSet(self, boardpos, block):
		#print boardpos, BOARDSIZE
		self.board[boardpos + BOARDSIZE] = block

	def boardUnSet(self, boardpos, block):
		self.board[boardpos + BOARDSIZE] = 0	

	def place(self, player, block, pos):
		if player == 0:
			blocks = self.myBlocks
		else:
			blocks = self.oppBlocks
		if (self.lookup(pos) == 0 and blocks[block-1] != 0):
			blocks[block - 1] = 0
			self.boardSet(pos, block)
		else:
			print "ERROR. Cannot place block "+ str(block) + " at position " + str(pos)
			if blocks[block-1] == 0 :
				print "Block ERROR " + str(block)
			else :
			    print "Pos Error " + str(pos)  

	def remove(self, player, block, pos):
		if player == 0:
			blocks = self.myBlocks
		else:
			blocks = self.oppBlocks
		if (self.lookup(pos) != 0 and blocks[block-1] == 0):
			blocks[block - 1] = block
			self.boardUnSet(pos, block)
		else:
			print "ERROR. Cannot remove block " + str(block) + " from position " + str(pos)
			if blocks[block-1] == 0 :
				print "Block ERROR " + str(block)
			else :
			    print "Pos Error " + str(pos)  



	def calcTorques(self):
		self.torqueA = -SUPPORTA * BOARDWEIGHT
		self.torqueB = -SUPPORTB * BOARDWEIGHT
		for i in range (-BOARDSIZE, BOARDSIZE+1):
			dista = i - SUPPORTA
			distb = i - SUPPORTB
			self.torqueA += self.lookup(i) * dista
			self.torqueB += self.lookup(i) * distb

	def freeSpots(self):
		return [i for i in range(-BOARDSIZE, BOARDSIZE +1) if self.lookup(i) == 0]

	def blocksleft(self, player):
		if player == 0:
			blocks = self.myBlocks
		else:
			blocks = self.oppBlocks
		return [i + 1 for i in range(self.k) if blocks[i] != 0]


	def tip(self):
		self.calcTorques()
		return (self.torqueA < 0 or self.torqueB > 0)


def boardTest():
	b = Board(15)
	turn = 0
	print "Torque on support A: " + str(b.torqueA)
	print "Torque on support B: " + str(b.torqueB) + "\n"
	while (not b.tip()):
		index = np.random.choice(b.blocksleft(turn))
		spot = np.random.choice(b.freeSpots())
		b.place(turn, index, spot)
		b.calcTorques()
		print "Player " + str(turn + 1) + " places weight " + str(index) + " at position " + str(spot)
		print "Torque on support A: " + str(b.torqueA)
		print "Torque on support B: " + str(b.torqueB) + "\n"



#boardTest()


	