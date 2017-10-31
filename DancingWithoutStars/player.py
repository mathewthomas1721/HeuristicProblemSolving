#!/usr/bin/python
import sys, random
import numpy as np
from client import Client
from getopt import getopt, GetoptError

"""
python3 sample_player.py -H <host> -p <port> <-c|-s>
"""
def manhattan_distance(x1, y1, x2, y2):
  return abs(x1 - x2) + abs(y1 - y2)

def process_file(file_data):
  """read in input file"""
  dancers = list()
  f = file_data.split("\n")
  for line in f:
    tokens = line.split()
    if len(tokens) == 2:
      dancers.append([int(tokens[0]), int(tokens[1])])

  return dancers

def formatting(unformat, c, k):
    formattedData = []
    for i in range(k):
        for j in range(c):
            formattedData.append(unformat[(j*k)+i])
    return np.array(formattedData)

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
'''def get_stars(dancers, k, board_size, num_color):
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
  return stars_str'''

def get_stars(boardData, size, k, c):
    superSet = []
    for i in range(size):
        for j in range(size):
            superSet.append([i,j])
    superSet = np.array(superSet)

    boardData.sort()

    a1_rows = superSet.view([('', superSet.dtype)] * superSet.shape[1])
    a2_rows = boardData.view([('', boardData.dtype)] * boardData.shape[1])
    freeSet = np.setdiff1d(a1_rows, a2_rows).view(superSet.dtype).reshape(-1, superSet.shape[1])

    stars = []
    while len(stars)<k:
        choice = random.choice(freeSet)
        check = 1
        for star in stars :
            if manhattan_distance(choice[0],choice[1],star[0],star[1]) <= c:
                check = -1
                break
        if check == 1:
            stars.append(list(choice))
    return np.array(stars)

# TODO add your method here
'''def get_a_move(dancers, stars, k, board_size, num_color):
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
  return "5 " + move'''

def checkerBoardGraph(board_size):
    cBG = []
    for i in range(board_size):
        for j in range(board_size):
            if i < board_size-1:
                cBG.append((str(i) + "," + str(j), str(i+1) + "," + str(j), 1))
                cBG.append((str(i+1) + "," + str(j), str(i) + "," + str(j), 1))
            if j < board_size-1:
                cBG.append((str(i) + "," + str(j), str(i) + "," + str(j+1), 1))
                cBG.append((str(i) + "," + str(j+1), str(i) + "," + str(j), 1))
            if i >= 0:
                cBG.append((str(i) + "," + str(j), str(i-1) + "," + str(j), 1))
                cBG.append((str(i-1) + "," + str(j), str(i) + "," + str(j), 1))
            if j >= 0:
                cBG.append((str(i) + "," + str(j), str(i) + "," + str(j-1), 1))
                cBG.append((str(i) + "," + str(j-1), str(i) + "," + str(j), 1))
    return cBG

def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen = [(0,f,())], set()
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost+c, v2, path))

def main():
  # create client
  host,port,player = get_args()
  client = Client(host, port)
  # send team name
  client.send("BabySnakes")
  # receive other parameters
  parameters = client.receive()
  parameters_l = parameters.split()
  board_size = int(parameters_l[0])
  num_color = int(parameters_l[1])
  k = int(parameters_l[2]) # max num of stars
  # receive file data
  file_data = client.receive()
  #print (file_data)
  # process file
  dancers_unformat = process_file(file_data) # a set of initial dancers
  dancers_format = formatting(dancers_unformat,num_color,k)
  # now start to play
  #stars1 = stars(dancers_format, board_size,k,num_color)
  #dancers = [list(elem) for elem in dancers]
  #print(stars1)
  #print(k)
  if player == "s":
    stars1 = get_stars(dancers_format, board_size,k,num_color)
    stars1 = ' '.join(str(r) for v in stars1 for r in v)
    print(stars1)
    client.send(stars1)
  else: # choreographer
    stars_str = client.receive()
    stars_str_l = stars_str.split()
    stars = set()
    for i in range(int(len(stars_str_l)/2)):
      stars.add((int(stars_str_l[2*i]), int(stars_str_l[2*i+1])))
    print("reached")
    '''for i in range(0, 1000): # send a thousand random moves
      move = get_a_move(dancers, stars, k, board_size, num_color)
      print(move)
      client.send(move)
    # send DONE flag
    client.send("DONE")
    # send a random line
    random_dancer = random.sample(dancers, 1)[0]
    client.send(str(random_dancer[0]) + " " + str(random_dancer[1]) + " " + str(random_dancer[0]) + " " + str(random_dancer[1] + 4))
    '''
  # close connection
  client.close()
  #print (checkerBoardGraph(50))'''

if __name__ == "__main__":
  main()
