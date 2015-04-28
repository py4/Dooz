# Dumb Agent for Dooz
# Artificial Intelligence
# Winter 2015

import sys
import socket
import copy

# Constants
FREE_SIGN = '-'
ADJACENCY_LIST = [[1,3,4],[0,2,4],[1,4,5],[0,4,6],[0,1,2,3,5,6,7,8],[2,4,8],[3,4,7],[4,6,8],[4,5,7]]
HOST_NAME = socket.gethostname()
MY_NUMBER = sys.argv[1]
#MY_NUMBER = 1
PORT_NUMBER = 2000+ int(MY_NUMBER)
BUFFER_SIZE = 1024
GAME_OVER_MESSAGE = "GameOver"
MAXIMUMDEPTH = 0

# Create Welcoming TCP Socket
welcoming_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
welcoming_socket.bind((HOST_NAME,PORT_NUMBER))
welcoming_socket.listen(1)
(agent_socket,address) = welcoming_socket.accept()

# Start the Game
my_step = 0
game_state = agent_socket.recv(BUFFER_SIZE)


###########################################

# Minimax Search
def terminal_test(game_board,turn):
    turn = str(3-int(turn))
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

def successors(state,turn,depth = 0):
    my_cells = [i for i, letter in enumerate(state) if letter == str(turn) ]
    all_suc=[]
    if int(MY_NUMBER) == 1:
        limit_depth_for_add = 5
    else:
        limit_depth_for_add = 4

    if depth <= limit_depth_for_add:
        for i in range(0,9):
               if  state[i]== FREE_SIGN:
                   new_state = copy.deepcopy(state)
                   new_state[i] = str(turn)
                   all_suc.append((new_state,str(i)))
    else:
        for i in range(len(my_cells)):
            for j in range(len(ADJACENCY_LIST[my_cells[i]])):
                if state[ADJACENCY_LIST[my_cells[i]][j]] == FREE_SIGN:
                    new_state = copy.deepcopy(state)
                    new_state[ADJACENCY_LIST[my_cells[i]][j]] = str(turn)
                    new_state[my_cells[i]] = FREE_SIGN
                    all_suc.append((new_state,str(my_cells[i]) + str(ADJACENCY_LIST[my_cells[i]][j])))
    return all_suc

def minimax_decision(state,turn,depth):
    global MAXIMUMDEPTH
    #print "in minimax,,,, and state is ",state[0]
    if int(terminal_test(state[0],turn)) == int(MY_NUMBER):
            #print "player ",int(turn),"is the winner"
            return (1,None)
    elif (int(terminal_test(state[0],turn))!=0) and (int(terminal_test(state[0],turn))!=int(MY_NUMBER)) :
            #print "player ",3-int(turn),"is the winner"
            return (-1,None)
    else:
        if int(depth) == MAXIMUMDEPTH:
            return (0,None)
    #check if is max_node
    if depth%2 == 0 :
        #print "MAX MOVE"
        best_move = None
        v = -10000
        children = successors(state[0],turn,depth)

        for child in children:
           #print "child[0] is",child[0]
           ans = minimax_decision((child[0],None),(3-turn),(depth+1))
           if(v<ans[0]):
                v = ans[0]
                best_move = str(child[1])
                if v == 1 :
                    return (v,best_move)
    else:
        #print "MIN MOVE"
        best_move = None
        v = 10000
        children = successors(state[0],turn,depth)
        for child in children:
            #print "child is",child
            ans = minimax_decision((child[0],None),3-turn,depth+1)
            if(v> ans[0] ):
                v = ans[0]
                best_move = child[1]
                if v==-1:
                    return (v,best_move)

    return (v,best_move)

def calc_depth(state):
    ones = 0
    twos = 0
    for i in state:
        if i == '-':
            continue
        else:
            if int(i)==1:
                ones+=1
            elif int(i)==2:
                twos+=1
    if int(MY_NUMBER)== 1:
        return ones+twos
    else:
        return ones+twos-1

#my_step = 0
while game_state != GAME_OVER_MESSAGE:
    game_state = list(game_state)
    stat = (game_state,None)
    dpt = int(calc_depth(stat[0]))
    if my_step >= 3:
        dpt = 10
    print "depth is ",dpt
    global MAXIMUMDEPTH
    MAXIMUMDEPTH = 6 + dpt
    next_move = str(minimax_decision(stat,int(MY_NUMBER),dpt)[1])
    print "next_move is " , next_move
    agent_socket.send(str(next_move))
    my_step+=1
    game_state = agent_socket.recv(BUFFER_SIZE)

agent_socket.close()