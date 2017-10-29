#!/usr/bin/python
import sys, random
from client import Client
from getopt import getopt, GetoptError

"""
python3 sample_player.py -H <host> -p <port> <-c|-s>
"""

def process_file(file_data):
  """read in input file"""
  dancers = set()
  f = file_data.split("\n")
  for line in f:
    tokens = line.split()
    if len(tokens) == 2:
      dancers.add((int(tokens[0]), int(tokens[1])))
  return dancers

def print_usage():
  print("Usage: python3 sample_player.py -H <host> -p <port>")

def get_args():
  host = None
  port = None
  player = None
  try:
    opts, args = getopt(sys.argv[1:], "hcsH:p:", ["help"])
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
    elif opt == "-c":
      player = "c"
    elif opt == "-s":
      player = "s"
  if host is None or port is None or player is None:
    print_usage()
    sys.exit(2)
  return host, port, player

# TODO add your method here
def get_stars(dancers, k, board_size, num_color):
  stars = set()
  x = -1
  y = -1
  while len(stars) < k:
    x = random.randint(0, board_size - 1)
    y = random.randint(0, board_size - 1)
    if (x, y) not in dancers and (x, y) not in stars:
      # check manhattan distance with other stars
      ok_to_add = True
      for s in stars:
        if abs(x - s[0]) + abs(y - s[1]) < num_color + 1:
          ok_to_add = False
          break
      if ok_to_add:
        stars.add((x, y))
  stars_str = ""
  for s in stars:
    stars_str += (str(s[0]) + " " + str(s[1]) + " ")
  return stars_str

# TODO add your method here
def get_a_move(dancers, stars, k, board_size, num_color):
  # pick 5 random dancers from dancers
  count = 0
  moved = set()
  move = ""
  while count < 5:
    # pick random dancers
    picked = random.sample(dancers, 5 - count)
    for d in picked:
      x, y = d[0], d[1]
      if (x, y) in moved:
        continue
      c = random.sample([(1, 0), (-1, 0), (0, 1), (0, -1)], 1)[0]
      x2 = x + c[0]
      y2 = y + c[1]
      if (x2, y2) in dancers or (x2, y2) in stars:
        continue
      if x2 not in range(board_size) or y2 not in range(board_size):
        continue
      move += (str(x) + " " + str(y) + " " + str(x2) + " " + str(y2) + " ")
      dancers.remove((x, y))
      dancers.add((x2, y2))
      moved.add((x2, y2))
      count += 1
  return "5 " + move

def main():
  host, port, player = get_args()
  # create client
  client = Client(host, port)
  # send team name
  client.send("SamplePlayer")
  # receive other parameters
  parameters = client.receive()
  parameters_l = parameters.split()
  board_size = int(parameters_l[0])
  num_color = int(parameters_l[1])
  k = int(parameters_l[2]) # max num of stars
  # receive file data
  file_data = client.receive()
  # process file
  dancers = process_file(file_data) # a set of initial dancers
  # now start to play
  if player == "s":
    # TODO modify here
    stars = get_stars(dancers, k, board_size, num_color)
    print(stars)
    # send stars
    client.send(stars)
  else: # choreographer
    # TODO modify here
    # receive stars from server
    stars_str = client.receive()
    stars_str_l = stars_str.split()
    stars = set()
    for i in range(int(len(stars_str_l)/2)):
      stars.add((int(stars_str_l[2*i]), int(stars_str_l[2*i+1])))
    for i in range(0, 1000): # send a thousand random moves
      move = get_a_move(dancers, stars, k, board_size, num_color)
      print(move)
      client.send(move)
    # send DONE flag
    client.send("DONE")
    # send a random line
    random_dancer = random.sample(dancers, 1)[0]
    client.send(str(random_dancer[0]) + " " + str(random_dancer[1]) + " " + str(random_dancer[0]) + " " + str(random_dancer[1] + 4))

  # close connection
  client.close()

if __name__ == "__main__":
  main()