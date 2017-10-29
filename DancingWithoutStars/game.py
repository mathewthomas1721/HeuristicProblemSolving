#!/usr/bin/python
import sys, socket, time, os
from Server import Server
from copy import deepcopy
from getopt import getopt
from ui import update_state

"""
Usage: python3 game.py -H <host> -p <port> -f <filename> -s <size> [-u]\n
use -u to enable frontend
"""

class Game(object):

  def __init__(self, host, port, input_file, size):
    """Initialize game"""
    # read file input
    self.file_input, self.dancers = self.__process_input(input_file)
    # setup board
    self.board_size = size
    self.num_color = len(self.dancers)
    self.k = len(self.dancers[0]) # the max number of stars
    if self.k * (self.num_color + 1) >= self.board_size * self.board_size:
      print("Invalid board size! It needs to be bigger enough to contain all the dancers and stars!")
      sys.exit(2)
    self.board = self.__setup_board(self.dancers, size)
    self.stars = set()
    self.dancer_steps = 0
    # initialize server
    self.server, self.choreographer, self.spoiler = self.__setup_server(host, port)

  def __setup_server(self, host, port):
    server = Server(host, port)
    choreographer, spoiler = server.establish_connection()
    return server, choreographer, spoiler # return server and both players' name

  def __process_input(self, filename):
    """read in input file"""
    f = open(filename)
    file_input = ""
    dancers = list()
    cur = -1
    for line in f:
      file_input += line
      tokens = line.split()
      if len(tokens) == 0:
        continue # skip empty lines
      elif len(tokens) == 2:
        dancers[cur].append((int(tokens[0]), int(tokens[1])))
      else:
        cur = int(tokens[len(tokens) - 1]) - 1
        dancers.append(list())
    return file_input, dancers

  def __setup_board(self, dancers, size):
    """Initialize board"""
    # fill all the space with 0
    board = [[0 for i in range(size)] for j in range(size)]
    # fill in all the dancers with their colors
    for index in range(len(dancers)):
      for pos in dancers[index]:
        if self.__inside_board(pos[0], pos[1]):
          board[pos[0]][pos[1]] = index + 1
        else:
          print("Initial position " + str(pos[0]) + ", " + str(pos[1]) + " not inside board! Check input file!")
          sys.exit(2)
    return board

  def __inside_board(self, x, y):
    """check if this position is inside board"""
    if x not in range(self.board_size) or y not in range(self.board_size):
      return False
    return True

  def __manhattan_distance(self, x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

  def __is_star_valid(self, x, y):
    """
    Check if it is valid to place a start at this position\n
    1. Star can be only placed in an empty spot\n
    2. two stars cannot closer then c+1 manhattan distance
    """
    # if it is a valid position on board
    if not self.__inside_board(x, y):
      print("Star not inside board")
      return False # outside board
    # check if it is an empty spot
    if self.board[x][y] == 0:
      valid = True
      # check manhattan distance with other stars
      for s in self.stars:
        if self.__manhattan_distance(s[0], s[1], x, y) < self.num_color + 1:
          print("Manhattan distance not satisfied with " + str(s[0]) + ", " + str(s[1]))
          valid = False # manhattan distance can't smaller than c + 1
          break
      return valid
    else: # not an empty spot
      return False

  def __is_dancer_move_valid(self, start_x, start_y, end_x, end_y):
    """
    Check if this dancer move is valid\n
    1. dancer can only move 1 row-wise or col-wise\n
    2. dancer cannot move to a position that has a star\n
    3. dancer cannot move to a position outside the board
    """
    if self.__manhattan_distance(start_x, start_y, end_x, end_y) > 1:
      print("Dancer can only move 1 row-wise or col-wise")
      return False
    # check if both positions are inside the board
    elif not (self.__inside_board(start_x, start_y) and self.__inside_board(end_x, end_y)):
      print("Position outside board")
      return False # one of points outside board
    # check if there is a dancer at the start position
    elif self.board[start_x][start_y] in (0, -1):
      print("no dancer at this start location")
      return False # no dancer at this location
    # check if the dancer will move to a star
    elif self.board[end_x][end_y] == -1:
      print("There is a star at end location")
      return False # there is a star at end location
    else:
      return True

  def __check_finish(self, lines):
    """check if the current game is finished"""
    checked = set()
    # go through the lines
    finished = True
    for line in lines:
      # get the points
      start_x = int(line[0])
      start_y = int(line[1])
      end_x = int(line[2])
      end_y = int(line[3])
      # get direction
      if end_x-start_x == 0:
        direct_x = 0
      else:
        direct_x = int((end_x-start_x) / abs(end_x-start_x))
      if end_y-start_y == 0:
        direct_y = 0
      else:
        direct_y = int((end_y-start_y) / abs(end_y-start_y))
      if direct_x != 0 and direct_y != 0:
        # if they both not equals to 0
        # then it means the moving direction
        # is not vertical or horizontal
        print("Invalid moving direction for line (" + str(start_x) + ", " + str(start_y) + ")--(" + str(end_x) + ", " + str(end_y) + ")")
        finished = False
        break
      cur_x = start_x
      cur_y = start_y
      colors = set()
      valid_line = True
      while True:
        if (cur_x, cur_y) in checked:
          print("Reuse dancer " + str(cur_x) + ", " + str(cur_y) + " in line (" + str(start_x) + ", " + str(start_y) + ")--(" + str(end_x) + ", " + str(end_y) + ")")
          valid_line = False
          break
        checked.add((cur_x, cur_y))
        c = self.board[cur_x][cur_y]
        if c in (0, -1):
          print("No dancer at position " + str(cur_x) + ", " + str(cur_y) + " for line (" + str(start_x) + ", " + str(start_y) + ")--(" + str(end_x) + ", " + str(end_y) + ")")
          valid_line = False
          break
        if c in colors:
          print("Duplicate color " + str(c) + " found for line (" + str(start_x) + ", " + str(start_y) + ")--(" + str(end_x) + ", " + str(end_y) + ")")
          valid_line = False
          break
        colors.add(c)
        if cur_x == end_x and cur_y == end_y:
          break # this line is all checked
        cur_x += direct_x
        cur_y += direct_y
      # check if that was a valid line
      if not valid_line:
        finished = False
        break
      # check if this line contains all the colors
      if len(colors) != self.num_color:
        print("Missing color in line (" + str(start_x) + ", " + str(start_y) + ")--(" + str(end_x) + ", " + str(end_y) + ")")
        finished = False
        break
    # finished checking all the lines
    # see if the state is still good
    if not finished:
      return False
    # now check if all the dancers has been in the lines
    for c in self.dancers:
      error = False
      for d in c:
        if (d[0], d[1]) not in checked:
          error = True
          print("(" + str(d[0]) + ", " + str(d[1]) + ") not in any line")
          break
      if error:
        finished = False
        break
    return finished

  def __place_stars(self, stars):
    """
    Place a list of stars on the board\n
    return true if success and false and error message if fail
    """
    success = True
    msg = None
    for s in stars:
      if self.__is_star_valid(s[0], s[1]):
        self.stars.add(s)
        self.board[s[0]][s[1]] = -1 # mark it on board
      else:
        success = False
        msg = "Spoiler placed an invalid star at: " + str(s[0]) + ", " + str(s[1])
        break
    return success, msg
  
  def __update_dancers(self, moves):
    """
    Make a list of parallel movements.\n
    Those movements count as 1 step since they happen at the same time.\n
    1. go through all the moves and check if there is an invalid case:
      - there is no dancer from the start position
      - the move is more than 1 manhattan distance
      - the dancer is moving to a star
    2. check if there is any tile contains more than 1 dancers.
    Finally update tmp_board to self.board
    """
    self.dancer_steps += 1
    success = True
    msg = None
    # copy the current board into a three dimensional board
    # and only contain dancers
    # so that one spot can contain more than 1 dancers
    tmp_board = list()
    for i in range(self.board_size):
      tmp_board.append(list()) # append the ith list
      for j in range(self.board_size):
        tmp_board[i].append(list()) # append the jth
        if self.board[i][j] not in (0, -1): # not adding empty space or star
          tmp_board[i][j].append(self.board[i][j])        

    # for each move
    for (x1, y1, x2, y2) in moves:
      # check if this is a valid move
      if self.__is_dancer_move_valid(x1, y1, x2, y2):
        # make the move
        # update self.dancers
        color = self.board[x1][y1]
        self.dancers[color-1].remove((x1, y1))
        self.dancers[color-1].append((x2, y2))
        # update tmp_board
        tmp_board[x1][y1].remove(color)
        tmp_board[x2][y2].append(color)
      else:
        success = False
        msg = "Choreographer made an invalid move from " + str(x1) + ", " + str(y1) \
          + " to " + str(x2) + ", " + str(y2)
        break

    # finally check if there is more than 1 dancers in a spot
    # and update tmp_board to self.board
    break_signal = False
    for i in range(self.board_size):
      for j in range(self.board_size):
        # skip star since it will be check while making the moves
        if self.board[i][j] == -1:
          continue
        # check if there is more than 1 dancers in this spot
        if len(tmp_board[i][j]) > 1:
          success = False
          break_signal = True
          msg = "Choreographer made an invalid step, multiple dancers found in spot " + str(i) + ", " + str(j)
          break
        # now update to self.board
        if len(tmp_board[i][j]) == 0:
          self.board[i][j] = 0
        else: # length == 1
          self.board[i][j] = tmp_board[i][j][0]
      if break_signal:
        break

    return success, msg

  def get_board(self):
    """Get the current board"""
    return self.board

  def start_game(self, using_ui):
    # send parameters to both players
    # board size, numOfColor, k
    print("Sending other parameters to both players...")
    self.server.send_all(str(self.board_size) + " " + str(self.num_color) + " " + str(self.k))

    # send input file to both players
    print("Sending input file to both players...")
    self.server.send_all(self.file_input)

    # now wait for spoiler to send stars
    print("Waiting for spoiler to send the stars...")
    if using_ui:
      update_state(self.board_size, self.num_color, self.choreographer, \
        self.spoiler, "Waiting for the stars...", self.get_board(), True)
    start_time = time.time()
    star_data = ""
    while not star_data:
      if time.time() - start_time > 120:
        if using_ui:
          update_state(self.board_size, self.num_color, self.choreographer, \
            self.spoiler, "Waiting for the stars...", self.get_board(), False)
        print("Spoiler exceeds time limit!")
        self.server.close()
        sys.exit()
      star_data = self.server.receive(1)
    print(star_data)
    print("Received stars!")
    if using_ui:
      update_state(self.board_size, self.num_color, self.choreographer, \
        self.spoiler, "Received stars!", self.get_board(), False)

    # parse stars
    s_list = star_data.split()
    stars = list()
    for i in range(int(len(s_list)/2)):
      stars.append((int(s_list[2*i]), int(s_list[2*i+1])))
    print(stars)

    print("Adding stars to the board...")
    # process stars
    success, msg = self.__place_stars(stars)
    if not success:
      print(msg)
      if using_ui:
        update_state(self.board_size, self.num_color, self.choreographer, \
          self.spoiler, msg, self.get_board(), False)
      self.server.close()
      sys.exit()
    print("Done.")
    if using_ui:
      update_state(self.board_size, self.num_color, self.choreographer, \
        self.spoiler, "Stars added to board.", self.get_board(), False)

    # send stars to choreographer
    print("Sending stars to the choreographer...")
    self.server.send_to(0, star_data)

    # receive moves from choreographer
    print("Receiving moves from choreographer...")
    if using_ui:
      update_state(self.board_size, self.num_color, self.choreographer, \
        self.spoiler, "Receiving moves from choreographer...", self.get_board(), True)
    start_time = time.time()
    move_data = list()
    while True:
      if time.time() - start_time > 120:
        if using_ui:
          update_state(self.board_size, self.num_color, self.choreographer, \
            self.spoiler, "Choreographer exceeds time limit!", self.get_board(), False)
        print("Choreographer exceeds time limit!")
        self.server.close()
        sys.exit()
      # receive data
      data = self.server.receive(0)
      if not data:
        continue
      print(data)
      if data == "DONE": # received DONE flag
        break
      move_data += data.split()

    print("Receiving all the final state line infos...")
    if using_ui:
      update_state(self.board_size, self.num_color, self.choreographer, \
        self.spoiler, "Receiving all the final state line infos...", self.get_board(), False)
    line_info = ""
    while not line_info:
      line_info = self.server.receive(0)
    print(line_info)

    self.server.close()

    # parse move data
    steps = list()
    while len(move_data) != 0:
      # get the move count
      c = int(move_data.pop(0))
      moves = list()
      for i in range(c):
        x1 = move_data.pop(0)
        y1 = move_data.pop(0)
        x2 = move_data.pop(0)
        y2 = move_data.pop(0)
        moves.append([int(x1), int(y1), int(x2), int(y2)])
      steps.append(moves)
    
    # now execute the moves
    print("executing the moves...")
    for m in steps:
      move_success, msg = self.__update_dancers(m)
      if not move_success:
        print(msg) # invalid move
        update_state(self.board_size, self.num_color, self.choreographer, \
          self.spoiler, msg, self.get_board(), False)
        sys.exit()
      if using_ui:
        update_state(self.board_size, self.num_color, self.choreographer, \
          self.spoiler, "executing the moves...", self.get_board(), False)
        time.sleep(1)

    # parse line_info
    li_l = line_info.split()
    lines = list()
    if len(li_l) % 4 != 0:
      print("Incorrect data length!")
      sys.exit(2)
    for i in range(int(len(li_l)/4)):
      lines.append((li_l[4*i], li_l[4*i+1], li_l[4*i+2], li_l[4*i+3]))
    
    # check if the choreographer has reached the goal
    if self.__check_finish(lines):
      print("Game finished!")
      print(self.choreographer + " has taken " + str(self.dancer_steps) + " steps.")
      if using_ui:
        update_state(self.board_size, self.num_color, self.choreographer, \
          self.spoiler, self.choreographer + " has taken " + str(self.dancer_steps) + " steps.", self.get_board(), False)
    else:
      print("Game finished!")
      print(self.choreographer + " didn't reach the goal.")
      if using_ui:
        update_state(self.board_size, self.num_color, self.choreographer, \
          self.spoiler, self.choreographer + " didn't reach the goal.", self.get_board(), False)

def print_usage():
  print("Usage: python3 game.py -H <host> -p <port> -f <filename> -s <size>")

def main():
  host = None
  port = None
  filename = None
  size = None
  using_ui = False
  try:
    opts, args = getopt(sys.argv[1:], "huH:p:f:s:", ["help"])
  except GetoptError:
    print_usage()
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print_usage()
      sys.exit()
    elif opt == "-H":
      host = arg
    elif opt == "-p":
      port = int(arg)
    elif opt == "-f":
      filename = arg
    elif opt == "-s":
      size = int(arg)
    elif opt == "-u":
      using_ui = True
  # initialize game    
  game = Game(host, port, filename, size)
  # run game
  game.start_game(using_ui)

if __name__ == "__main__":
  main()