# Dumb Agent for Dooz
# Artificial Intelligence
# Winter 2015

import sys
import socket
from tree import *

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

welcoming_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
welcoming_socket.bind((HOST_NAME,PORT_NUMBER))
welcoming_socket.listen(1)
(agent_socket,address) = welcoming_socket.accept()
game_state = agent_socket.recv(BUFFER_SIZE)

def state_key(game_state):
    return ''.join(game_state)

def count_chars(game_state):
    return len([el for el in game_state if el == MY_NUMBER])

def get_diff(arr1, arr2):
    diffs = []
    for i,el in enumerate(arr1):
        if(el == '-' and arr2[i] == '1' or (el == '1' and arr2[i] == '-')):
            diffs.append(i)
    return diffs

def decide(game_state, state_repository):
    old_state = state_key(game_state)
    print "old_state:  "+str(old_state)
    new_state = state_repository[old_state+str(MY_NUMBER)][0:9]
    print "new_state:  "+str(new_state)
    if(count_chars(game_state) < 3):
        diff = get_diff(old_state, new_state)
        if(len(diff) > 1):
            print "FUCK!"
        return str(diff[0])
    else:
        diff = get_diff(old_state, new_state)
        print "diff:  "
        print diff
        if(len(diff) > 2):
            print "FUCK2!"
        if(old_state[diff[0]] == '-'):
            return str(diff[1])+str(diff[0])
        if(new_state[diff[0]] == '1'):
            return str(diff[0])+str(diff[1])


#root_node.dump()
node, evaluated_nodes, state_repository = build_tree()

while game_state != GAME_OVER_MESSAGE:
    move = decide(game_state, state_repository)
    agent_socket.send(str(move))
    game_state = agent_socket.recv(BUFFER_SIZE)

agent_socket.close()
welcoming_socket.close()
