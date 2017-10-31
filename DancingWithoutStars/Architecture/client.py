import socket


class Client(object):
    
  def __init__(self, host, port):
    """Initialize client and connect"""
    self.cache = list()
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((host, port))
    print("Connected to server.")

  def send(self, data):
    """send data to server"""
    self.socket.sendall(bytes(data + "&", "utf-8"))

  def receive(self):
    """receive data from server"""
    if len(self.cache) > 0:
      return self.cache.pop(0)
    else:
      # keep receive until the last char is &
      data = ""
      while True:
        data += self.socket.recv(4096).decode("utf-8")
        if len(data) > 0 and data[-1] == "&":
          break
      self.cache += list(filter(None, data.split("&")))
      return self.cache.pop(0)

  def close(self):
    self.socket.close()