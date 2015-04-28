# Dumb Agent for Dooz
# Artificial Intelligence
# Winter 2015

import sys
import socket


# Constants
FREE_SIGN = '-'
ADJACENCY_LIST = [[1,3,4],[0,2,4],[1,4,5],[0,4,6],[0,1,2,3,5,6,7,8],[2,4,8],[3,4,7],[4,6,8],[4,5,7]]
HOST_NAME = socket.gethostname()
MY_NUMBER = sys.argv[1]
PORT_NUMBER = 2000 + int(MY_NUMBER)
BUFFER_SIZE = 1024
GAME_OVER_MESSAGE = "GameOver"
MAX_STEP = 100
# Create Welcoming TCP Socket

#welcoming_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#welcoming_socket.bind((HOST_NAME,PORT_NUMBER))
#welcoming_socket.listen(1)
#(agent_socket,address) = welcoming_socket.accept()
my_step = 0
#game_state = agent_socket.recv(BUFFER_SIZE)

def decide(game_state):
  if my_step <= 2:
    next_move = game_state.find(FREE_SIGN)
  else:
    my_cells = [i for i, letter in enumerate(game_state) if letter == MY_NUMBER]
    for i in range(len(my_cells)):
      for j in range(len(ADJACENCY_LIST[my_cells[i]])):
        if game_state[ADJACENCY_LIST[my_cells[i]][j]] == FREE_SIGN:
	  next_move = str(my_cells[i]) + str(ADJACENCY_LIST[my_cells[i]][j])
	  break
  return next_move


root_node = build_tree()
#root_node.dump()

#while game_state != GAME_OVER_MESSAGE:
#  agent_socket.send(str(decide(game_state)))
#  my_step += 1
#  game_state = agent_socket.recv(BUFFER_SIZE)

agent_socket.close()
