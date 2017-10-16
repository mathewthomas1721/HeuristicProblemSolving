import socket, time, random, sys, math, copy
import numpy as np
import Grav_Voronoi

class Client:
  def __init__(self, host, port, name):
    self.host = host
    self.port = port
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.name = name

    # hard-coded game info
    self.grid_size = 1000
    self.min_dist = 66

    # connect to server and get game info
    self.sock.connect((host, port))
    self.num_players, self.num_stone, self.player_number = map(int, self.__receive_move())
    self.score_grid = np.zeros((self.grid_size, self.grid_size), dtype=np.int)
    self.pull = np.zeros((self.num_players, self.grid_size, self.grid_size), dtype=np.float32)

    self.row_numbers = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
    for i in range(self.grid_size):
      self.row_numbers[i] = self.row_numbers[i] + i
    self.col_numbers = np.transpose(self.row_numbers)
    self.scores = [0] * self.num_players

    self.moves = [] # store history of moves
    
    # send name to serer
    self.__send(self.name)
    print("Client initialized")

  def __receive(self):
    return self.sock.recv(2048).decode('utf-8')
  
  def __send(self, string):
    self.sock.sendall(string.encode('utf-8'))

  def __receive_move(self):
    return self.__receive().split()

  def __send_move(self, move_row, move_col):
    self.__send("{} {}".format(move_row, move_col))

  def __compute_distance(self, row1, col1, row2, col2):
    return math.sqrt((row2 - row1)**2 + (col2 - col1)**2)

  def __is_valid_move(self, move_row, move_col):
    for move in self.moves:
      if (self.__compute_distance(move_row, move_col, move[0], move[1])) < self.min_dist:
        return False
    return True

  def compute_pull(self, row, col):
    # squared_distance_matrix[i][j] is the squared distance from (i, j) to (row, col)
    squared_distance_matrix = np.square(self.row_numbers - row) + np.square(self.col_numbers - col)
    # This value would otherwise have been 0 and would therefore have caused an exception when taking the reciprocal
    squared_distance_matrix[row][col] = 0.1e-30
    # After taking the reciprocal it correctly indicates the pull added at at (i, j) by having a stone at (row, col)
    return np.reciprocal(squared_distance_matrix)    


  def __update_scores(self, move_row, move_col, player):
    # Add pull from new stone to current pull
    self.pull[player] = self.pull[player] + self.compute_pull(move_row, move_col)
    # Update each point in the grid to be owned by the player with the highest pull
    self.score_grid = np.argmax(self.pull, axis=0) + 1

    # For each player set the score to be the sum of owned squares on the grid
    for i in range(self.num_players):
      self.scores[i] = np.sum(self.score_grid == (i+1))

  # your algorithm goes here
  # a naive random algorithm is provided as a placeholder

  def __min_min_dist(self, row, col, max_min):
    e1 = np.abs(self.grid_size - row - 1.0)
    e2 = np.abs(self.grid_size - col - 1.0)
    e3 = float(row)
    e4 = float(col)

    minE = min(e1, e2, e3, e4)
    if minE <= max_min:
      return max_min
    new_min = minE

    for move in self.moves:
      d = self.__compute_distance(row,col, move[0], move[1])
      if d < max_min:
        return max_min
      elif d < new_min:
        new_min = d
    return new_min

  def __getMoveCloseCenter(self):
    min_dist_to_center = 1000.0
    min_dist_r, min_dist_c = 0,0
    for row in range(self.grid_size):
      for col in range(self.grid_size):
        if (self.__is_valid_move(row, col)):
          d = self.__compute_distance(row,col, 499, 499)
          if d < min_dist_to_center:
            min_dist_to_center = d
            min_dist_r = row
            min_dist_c = col
    return min_dist_r, min_dist_c


  def __getMoveMaxMinDist(self):
    max_dist = float(self.min_dist)
    max_r, max_c = 0,0
    for row in range(self.grid_size):
      for col in range(self.grid_size):
        d = self.__min_min_dist(row,col, max_dist)
        if d > max_dist:
          max_r, max_c = row, col
          max_dist = d
    print(max_dist, max_r, max_c, self.__min_min_dist(max_r, max_c, 55.0))
    return max_r, max_c


  def __getMoveGreedy(self):
    bestMove = (0,0)
    bestScore = 0
    old_score_grid = copy.deepcopy(self.score_grid)
    old_pull = copy.deepcopy(self.pull)
    old_scores = copy.deepcopy(self.scores)
    for row in range(self.grid_size):
      print(row)
      for col in range(self.grid_size):
        if (self.__is_valid_move(row, col)):
          self.__update_scores(row,col, self.player_number - 1)
          if bestScore < self.scores[self.player_number - 1]:
            bestScore = self.scores[self.player_number - 1]
            bestMove = (row,col)
        self.score_grid = copy.deepcopy(old_score_grid)
        self.pull = copy.deepcopy(old_pull)
        self.scores = copy.deepcopy(old_scores)
    return bestMove[0], bestMove[1]

  def __getMove(self):
    move_row = 0
    move_col = 0
    while True:
      move_row = random.randint(0, 999)
      move_col = random.randint(0, 999)
      if (self.__is_valid_move(move_row, move_col)):
        break
    
    return move_row, move_col
  
  def start(self):
    while True:
      move_data = self.__receive_move()
      # check if game is over
      if int(move_data[0]) == 1:
        print("Game over")
        break

      # scores
      scores = []
      for i in range(self.num_players):
        scores.append(move_data[i + 1])
      # new moves
      new_moves = move_data[self.num_players + 1 : ]
      num_new_moves = int(len(new_moves) / 3)
      # sanity check
      if num_new_moves * 3 != len(new_moves):
        print("Error: error parsing list of new moves")
      
      # insert new moves into the grid
      for i in range(num_new_moves):
        move_row = int(new_moves[3 * i])
        move_col = int(new_moves[3 * i + 1])
        player = int(new_moves[3 * i + 2])
        # sanity check, this should always be true
        if player > 0:
          self.moves.append((move_row, move_col, player))
          self.__update_scores(move_row, move_col, player - 1)

        else:
          print("Error: player info incorrect")

      # make move
      if (self.player_number == 2):
        my_move_row, my_move_col = self.__getMoveMaxMinDist()
      else:
        my_move_row, my_move_col = self.__getMoveCloseCenter()
      self.moves.append((my_move_row, my_move_col, self.player_number))
      self.__send_move(my_move_row, my_move_col)
      print("Played at row {}, col {}".format(my_move_row, my_move_col))
    
    self.sock.close()

if (__name__ == "__main__"):
  host = sys.argv[1]
  port = int(sys.argv[2])
  name = sys.argv[3]
  # note: whoever connects to the server first plays first
  client = Client(host, port, name)
  client.start()
