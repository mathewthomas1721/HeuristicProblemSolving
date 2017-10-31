import requests

# hard-coded function to send state to nodejs server
#state
#{
#  board_size : int,
#  num_color : int,
#  choreographer : string,
#  spoiler : string,
#  stage : string,
#  board: [[]]
#}
def update_state(board_size, num_color, chore, spoi, stage, board, timer):
  data = { \
    "board_size" : board_size, \
    "num_color" : num_color, \
    "choreographer" : chore, \
    "spoiler" : spoi, \
    "stage" : stage, \
    "board" : board, \
    "timer" : timer }
  try:
    r = requests.post("http://127.0.0.1:3000/", json=data)
  except RuntimeError:
    print("[ERROR] failed to update state to frontends!!!")