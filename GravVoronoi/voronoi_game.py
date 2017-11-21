from voronoi_server import VoronoiServer

import time, sys, math, socket

class VoronoiGame:
  def __init__(self, num_stones, num_players, grid_size, min_dist, host, port, use_graphic):
    # game variables
    self.num_stones = num_stones
    self.num_players = num_players
    self.grid_size = grid_size
    self.min_dist = min_dist # minimum distance allowed between stoens
    self.grid = [[0] * grid_size for i in range(grid_size)]
    self.score_grid = [[0] * grid_size for i in range(grid_size)]
    self.scores = [0] * num_players
    self.player_times = [120.0] * num_players
    # store moves played, each move corresponds to 3 entries
    self.moves = []
    # gravitational pull, pull[i] is 2d-array of the pull player i has in total
    self.pull = []
    for i in range(num_players):
      self.pull.append([[0] * grid_size for j in range(grid_size)])
    self.current_player = 0
    self.moves_made = 0
    self.game_over = False
    self.epsilon = 1e-9

    # server that communicates to client
    self.server = VoronoiServer(host, port, num_players)
    # socket connection to web front end (udp)
    self.use_graphic = use_graphic
    self.graphic_socket = None
    if use_graphic:
      self.graphic_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.graphic_socket.connect(('localhost', 8080))

  def __reset(self):
    # reset game after a round
    self.grid = [[0] * self.grid_size for i in range(self.grid_size)]
    self.score_grid = [[0] * self.grid_size for i in range(self.grid_size)]
    self.scores = [0] * num_players
    self.player_times = [120.0] * num_players
    self.moves = []
    self.pull = []
    for i in range(num_players):
      self.pull.append([[0] * self.grid_size for j in range(self.grid_size)])
    self.moves_made = 0
    self.game_over = False

  def __get_game_info(self):
    # game over flag
    game_info = ("1" if self.game_over else "0") + " "
    # scores
    game_info += " ".join(str(i) for i in self.scores) + " "
    # new moves - go through move history in reverse order and stop when a move by current player is found
    new_moves = []
    for i in range(len(self.moves) - 1, 1, -3):
      if (self.moves[i] == self.current_player + 1):
        break
      for j in range(3):
        new_moves.append(self.moves[i - 2 + j])
    game_info += " ".join(str(i) for i in new_moves) + "\n"
    return game_info

  def __broadcast_game_info(self):
    game_info = self.__get_game_info()
    if self.game_over:
      for i in range(num_players):
        self.server.send(game_info, i)
    else:
      self.server.send(game_info, self.current_player)

  def __generate_compressed_game_bitmap(self):
    # Compression format is start_index end_index (inclusive) player_owner
    bitmap = ''
    for score_row in self.score_grid:
      bitmap += '0 '
      for i in range(1, len(score_row)):
        if score_row[i] != score_row[i-1]:
          # End this compression range and start the next one
          bitmap += '{} {} {} '.format(str(i - 1), str(score_row[i-1]), str(i))
      # End the final range
      bitmap += '{} {} '.format(str(len(score_row) - 1), str(score_row[-1]))
    return bitmap

  def __generate_decompressed_game_bitmap(self, compressed_bitmap):
    # This was just written for testing correct (de)compression
    i = 0
    compressed_bitmap_array = compressed_bitmap.split(' ')
    decompressed_bitmap = ''
    for j in range(0, 10**7, 3):
      decompressed_bitmap += (compressed_bitmap_array[j + 2] + ' ') * (int(compressed_bitmap_array[j + 1]) - int(compressed_bitmap_array[j]) + 1)
      if compressed_bitmap_array[j + 1] == '999':
        i += 1
        if i == 1000:
          break
    return decompressed_bitmap

  def __send_update_to_node(self, move_row, move_col):
    data = self.__generate_compressed_game_bitmap()
    # Add rest of meta data
    data += ' '.join(map(lambda x : '{0:.2f}'.format(x), self.player_times)) + ' '
    data += ' '.join(map(str, self.scores)) + ' '
    data += '{} {} '.format(self.num_players, self.current_player + 1)
    data += '{} {}'.format(move_row, move_col)
    data += '\n' # signify the end of the message

    self.graphic_socket.sendall(data.encode('utf-8'))

  def __soft_reset_node(self):
    self.graphic_socket.sendall('soft-reset\n'.encode('utf-8'))

  def __compute_distance(self, row1, col1, row2, col2):
    return math.sqrt((row2 - row1)**2 + (col2 - col1)**2)

  def __is_legal_move(self, row, col):
    if self.grid[row][col] != 0:
      print("({}, {}) is already occupied".format(row, col))
      return False
    if row < 0 or row >= self.grid_size:
      print("({}, {}) is out of bounds".format(row, col))
      return False
    if col < 0 or col >= self.grid_size:
      print("({}, {}) is out of bounds".format(row, col))
      return False
    # check for min dist requirement
    for move_start in range(0, len(self.moves), 3):
      move_row = self.moves[move_start]
      move_col = self.moves[move_start + 1]
      if (self.__compute_distance(row, col, move_row, move_col) < self.min_dist):
        print("({}, {}) is less than 66 unit distances away from ({}, {})".format(row, col, move_row, move_col))
        return False

    return True

  def __get_player_move(self):
    player_name = self.server.names[self.current_player]
    player_time = self.player_times[self.current_player]
    print("Waiting for {}".format(player_name))
    print("They have {} seconds remaining".format(player_time))

    start_time = time.time()
    client_response = self.server.receive(self.current_player)
    end_time = time.time()
    self.player_times[self.current_player] -= (end_time - start_time)

    data = client_response.split()
    return int(data[0]), int(data[1])

  def __update_scores(self, move_row, move_col):
    tie_created = 0
    tie_broken = 0
    # note: score ignores stones, because each player has the same number of stones
    for row in range(self.grid_size):
      for col in range(self.grid_size):
        # avoid division by 0
        if (row == move_row and col == move_col):
          continue
        # update current player's pull
        d = self.__compute_distance(row, col, move_row, move_col)
        self.pull[self.current_player][row][col] += float(float(1) / (d*d))

        # first move claims every cell on the grid
        if self.moves_made == 1:
          self.score_grid[row][col] = self.current_player + 1
          self.scores[self.current_player] += 1
        # not first move
        else:
          old_occupier = self.score_grid[row][col]
          current_player_pull = self.pull[self.current_player][row][col]
          # tie: multiple players had equal pull on the cell
          if old_occupier == 0:
            # check if current player's pull is now bigger than everyone else's
            current_player_has_max_pull = True
            for p in range(self.num_players):
              if p != self.current_player and self.pull[p][row][col] > current_player_pull - self.epsilon:
                current_player_has_max_pull = False
                break
            # tie broken
            if (current_player_has_max_pull):
              self.score_grid[row][col] = self.current_player + 1
              self.scores[self.current_player] += 1
              tie_broken += 1
          # no tie, and cell is claimed by some other player
          elif old_occupier - 1 != self.current_player:
            old_occupier_pull = self.pull[old_occupier - 1][row][col]
            # current player and old player have equal pull, then cell is not owned by anyone
            if abs(current_player_pull - old_occupier_pull) <= self.epsilon:
              self.score_grid[row][col] = 0
              self.scores[old_occupier - 1] -= 1
              tie_created += 1
            # current player now has a greater pull, change owner to current player
            elif current_player_pull > old_occupier_pull:
              self.score_grid[row][col] = self.current_player + 1
              self.scores[old_occupier - 1] -= 1
              self.scores[self.current_player] += 1

    print("This move broke {} ties and created {} new ties\n".format(tie_broken, tie_created))

  def __declare_winner(self):
    max_score = -1
    winners = []
    for i in range(self.num_players):
      player_name = self.server.names[i]
      player_score = self.scores[i]
      if self.scores[i] == -1:
        print("Illegal move by {}".format(player_name))
      elif self.scores[i] == -2:
        print("{} timed out".format(player_name))
      else:
        print("{} score: {}".format(player_name, player_score))

      if player_score == max_score:
        winners.append(i + 1)
      elif player_score > max_score:
        max_score = player_score
        winners = [i + 1]

    if len(winners) == 1:
      print("\nWinner: {}".format(self.server.names[winners[0] - 1]))
    else:
      print("Tied between: ")
      for winner in winners:
        print(" ".join([self.server.names[w - 1] for w in winners]))

  def start(self):
    self.server.establish_connection(self.num_players, self.num_stones)
    if self.use_graphic:
      graphic_init_msg = '"NAME_SEPARATOR"'.join(self.server.names) + '\n'
      self.graphic_socket.sendall(graphic_init_msg.encode('utf-8'))
    print('\nStarting...\n')

    for p in range(self.num_players):
      self.current_player = p
      while True:
        self.current_player = self.current_player % self.num_players
        self.__broadcast_game_info()
        if (self.game_over):
          break

        # get and validate move
        move_row, move_col = self.__get_player_move()
        print("{} has placed their stone on: {}, {}".format(self.server.names[self.current_player] , move_row, move_col))
        if not self.__is_legal_move(move_row, move_col):
          self.scores[self.current_player] = -1
          self.game_over = True
          continue

        # move is legal, do some book-keeping
        self.moves_made += 1
        self.grid[move_row][move_col] = self.current_player + 1
        self.moves.append(move_row)
        self.moves.append(move_col)
        self.moves.append(self.current_player + 1)
        self.__update_scores(move_row, move_col)

        # send data to node server
        if self.use_graphic:
          self.__send_update_to_node(move_row, move_col)

        # check for game over conditions
        if self.player_times[self.current_player] < 0:
          self.scores[self.current_player] = -2
          self.game_over = True
        if self.moves_made == self.num_players * self.num_stones:
          self.game_over = True

        # switch player
        self.current_player += 1

      if self.use_graphic:
          self.graphic_socket.sendall('game over\n'.encode('utf-8'))
      self.__declare_winner()
      print("\nGame over")

      # do reset unless it's the last game
      if p != num_players - 1:
        time.sleep(2) # pause for 2 seconds in between games
        self.__reset()
        if (use_graphic):
          self.__soft_reset_node()

if __name__ == "__main__":
  GRID_SIZE = 1000
  MIN_DIST = 66
  num_stones = int(sys.argv[1])
  num_players = int(sys.argv[2])
  host = sys.argv[3]
  port = int(sys.argv[4])
  use_graphic = False
  if len(sys.argv) == 6 and int(sys.argv[5]) == 1:
    use_graphic = True

  game = VoronoiGame(num_stones, num_players, GRID_SIZE, MIN_DIST, host, port, use_graphic)
  game.start()
