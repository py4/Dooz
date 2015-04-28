# Dumber Agent for Dooz
# Artificial Intelligence
# Winter 2015

import sys
import socket 
from random import randint


# Constants
FREE_SIGN = '-'
ADJACENCY_LIST = [[1,3,4],[0,2,4],[1,4,5],[0,4,6],[0,1,2,3,5,6,7,8],[2,4,8],[3,4,7],[4,6,8],[4,5,7]]
HOST_NAME = socket.gethostname()
MY_NUMBER = sys.argv[1]
PORT_NUMBER = 2000 + int(MY_NUMBER)
BUFFER_SIZE = 1024
GAME_OVER_MESSAGE = "GameOver"

# Create Welcoming TCP Socket
welcoming_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
welcoming_socket.bind((HOST_NAME,PORT_NUMBER))
welcoming_socket.listen(1)
(agent_socket,address) = welcoming_socket.accept()

# Start the Game
my_step = 0
game_state = agent_socket.recv(BUFFER_SIZE)
while game_state != GAME_OVER_MESSAGE:
	if my_step <= 2:
		player_command = randint(0,8)
		while game_state[player_command] != FREE_SIGN:
			player_command = randint(0,8)
		next_move = str(player_command)
	else:
		stop = False
		while (stop == False):
			player_command_string = str(randint(0,8)) + str(randint(0,8))
			if (game_state[int(player_command_string[0])] == MY_NUMBER and \
				game_state[int(player_command_string[1])] == FREE_SIGN and \
				int(player_command_string[1]) in ADJACENCY_LIST[int(player_command_string[0])]):
				next_move = player_command_string
				stop = True

	agent_socket.send(next_move)
	my_step += 1
	game_state = agent_socket.recv(BUFFER_SIZE)

agent_socket.close()    
