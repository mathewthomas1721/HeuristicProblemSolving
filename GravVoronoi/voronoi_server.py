import socket

class VoronoiServer:
  def __init__(self, host, port, num_players):
    self.host = host
    self.port = port
    self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.my_socket.bind((self.host, self.port))
    self.connection = [None] * num_players
    self.address = [None] * num_players
    self.names = [None] * num_players

  def establish_connection(self, num_players, num_stones):
    self.my_socket.listen(2) # 2 backlogs (number of unaccepted connections allowed)
    for i in range(1, num_players + 1):
      print("Waiting for player " + str(i))
      self.connection[i - 1], self.address[i - 1] = self.my_socket.accept()
      self.send(str(num_players) + " " + str(num_stones) + " " + str(i) + "\n", i - 1)
      self.names[i - 1] = self.receive(i - 1).strip()
      print("Connection from Player " + self.names[i - 1] + " established.")

    input("Press Enter to start the game...")

  def send(self, string, player):
    self.connection[player].sendall(string.encode('utf-8'))

  def receive(self, player):
    while True:
      data = self.connection[player].recv(1024).decode('utf-8')
      if not data:
        continue
      return data
