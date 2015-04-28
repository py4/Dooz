# Dooz Server
# Artificial Intelligence
# Winter 2015

import sys
import socket
import time


# Constants
BORD_SIZE = 3
MAX_STEP = 100;
FREE_SIGN = '-'
ADJACENCY_LIST = [[1,3,4],[0,2,4],[1,4,5],[0,4,6],[0,1,2,3,5,6,7,8],[2,4,8],[3,4,7],[4,6,8],[4,5,7]]
PLAYER_1_PORT_NUMBER = 2001
PLAYER_2_PORT_NUMBER = 2002
BUFFER_SIZE = 1024
GAME_OVER_MESSAGE = "GameOver"


# Global Variables
game_step = 0
game_board = BORD_SIZE * BORD_SIZE * [FREE_SIGN]


# This Function Check Player Command
def isLegal(player_command_string,turn):
	if game_step <= 5:
		if 0 <= int(player_command_string) <= 8 and game_board[int(player_command_string)] == FREE_SIGN:
			return True

	if game_step >= 6:
		if (game_board[int(player_command_string[0])] == turn and \
			game_board[int(player_command_string[1])] == FREE_SIGN and \
			int(player_command_string[1]) in ADJACENCY_LIST[int(player_command_string[0])]):
			return True

	return False


# This Function Print Board
def printBoard():
	for i in range(len(game_board)):
		print(game_board[i]),
		if (i % BORD_SIZE == 2):
			print('\n')


# This Function Check Terminal Condition
def isGameOver(turn):
	if ((game_board[0] == game_board[1] == game_board[2] == turn) or \
		(game_board[3] == game_board[4] == game_board[5] == turn) or \
		(game_board[6] == game_board[7] == game_board[8] == turn) or \
		(game_board[0] == game_board[3] == game_board[6] == turn) or \
		(game_board[1] == game_board[4] == game_board[7] == turn) or \
		(game_board[2] == game_board[5] == game_board[8] == turn) or \
		(game_board[0] == game_board[4] == game_board[8] == turn) or \
		(game_board[2] == game_board[4] == game_board[6] == turn)):
		winner = turn
		return winner
	else:
		return False


# Connect to Agents
player_1_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
player_1_socket.connect((socket.gethostname(),PLAYER_1_PORT_NUMBER))
player_2_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
player_2_socket.connect((socket.gethostname(),PLAYER_2_PORT_NUMBER))


# Start the Game
winner = 0
foul = 0
while winner == 0 and foul == 0 and game_step < MAX_STEP:
	turn = str(game_step % 2 + 1)

	if turn == str(1):
		player_1_socket.send(''.join(game_board))
		player_command_string = player_1_socket.recv(BUFFER_SIZE)
	else:
		player_2_socket.send(''.join(game_board))
		player_command_string = player_2_socket.recv(BUFFER_SIZE)

	if isLegal(player_command_string,turn) == False:
		foul = turn
		break

	if game_step <= 5:
		game_board[int(player_command_string)] = turn
		print('Player ' + turn + ': ' + player_command_string)
	else:
		game_board[int(player_command_string[0])] = FREE_SIGN
		game_board[int(player_command_string[1])] = turn
		print('Player ' + turn + ': ' + player_command_string[0] + ' -> ' + player_command_string[1])

	printBoard()
	winner = isGameOver(turn)
	time.sleep(1)
	game_step += 1

player_1_socket.send(GAME_OVER_MESSAGE)
player_2_socket.send(GAME_OVER_MESSAGE)
print 'Winner: ' + str(winner)
print 'Who Fouled: ' + str(foul)

player_1_socket.close()
player_2_socket.close()
