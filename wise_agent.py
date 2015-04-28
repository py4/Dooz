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

class Node:
  def __init__(self):
    self.state = []
    self.parent = None
    self.children = []
    self.value = None

  def count_each(self):
    count_a = 0
    count_b = 0
    for el in self.state:
        if el == 'A':
            count_a += 1
        if el == 'B':
            count_b += 1
    return (count_a, count_b)

  def is_done(self):
    if ((self.state[0] == self.state[1] == self.state[2] != FREE_SIGN) or \
	    (self.state[3] == self.state[4] == self.state[5] != FREE_SIGN) or \
	    (self.state[6] == self.state[7] == self.state[8] != FREE_SIGN) or \
	    (self.state[0] == self.state[3] == self.state[6] != FREE_SIGN) or \
	    (self.state[1] == self.state[4] == self.state[7] != FREE_SIGN) or \
	    (self.state[2] == self.state[5] == self.state[8] != FREE_SIGN) or \
	    (self.state[0] == self.state[4] == self.state[8] != FREE_SIGN) or \
	    (self.state[2] == self.state[4] == self.state[6] != FREE_SIGN)):
        return True
    return False

  def is_moving_started(self, min_or_max):
    a_count = 0
    b_count = 0
    for el in self.state:
        if el == 'A':
            a_count += 1
        if el == 'B':
            b_count += 1
    if(min_or_max == 1 and a_count >= 3):
        return True
    if(min_or_max == 0 and b_count >= 3):
        return True
    return False

  def evaluate(self, min_or_max, step, node_repo):
    if(step == MAX_STEP):
        return 0
    if(self.is_done()):
        if(step % 2 == 0):
            return -1
        else:
            return 0

    if(min_or_max == 1):
        cells = [i for i, letter in enumerate(self.state) if letter == 'A']
    else:
        cells = [i for i, letter in enumerate(self.state) if letter == 'B']

    if not self.is_moving_started(min_or_max):
        free_cells = [i for i, letter in enumerate(self.state) if letter == FREE_SIGN]
        for j in free_cells:
            new_node = Node()
            new_node.parent = self
            new_node.state = list(self.state)
            if(min_or_max == 0):
                s = 'B'
            else:
                s = 'A'
            before = list(node_repo)
            new_node.state[j] = s
            print("diff:  ", set(before) - set(node_repo))
            if(new_node.count_each()[0] > 3 or new_node.count_each()[1] > 3):
                print "parent node:  ", self.state
                print "parent of parent:  ", self.parent.state
                print "child node:  ", new_node.state
                print "Holly!"
                sys.exit()

            node_repo.append(new_node)
            self.children.append(new_node)
    else:
        for i in range(len(cells)):
            for j in range(len(ADJACENCY_LIST[cells[i]])):
                if (self.state[ADJACENCY_LIST[cells[i]][j]] == FREE_SIGN):
                    new_node = Node()
                    new_node.parent = self
                    new_node.state = list(self.state)
                    if(min_or_max == 0):
                        s = 'B'
                    else:
                        s = 'A'
                    before = list(node_repo)
                    new_node.state[i] = FREE_SIGN
                    new_node.state[ADJACENCY_LIST[cells[i]][j]] = s
                    print("diff:  ", set(before) - set(node_repo))
                    self.children.append(new_node)
                    node_repo.append(new_node)
    arr = []
    for n in self.children:
        arr.append(n.evaluate(1-min_or_max, step+1, node_repo))
    if(min_or_max == 0):
        self.value = min(arr)
    else:
        self.value = max(arr)
    return self.value

  def dump(self):
    print("============== DUMPING ==============")
    print(self.state)
    print("============== CHILDREN =============")
    for n in self.children:
        print(n.state)
    print("=====================================")
    for n in self.children:
        n.dump()

def build_tree():
    node_repo = []
    step = 0
    node = Node()
    node.state = ['-','-','-','-','-','-','-','-','-']
    node.evaluate(0, step, node_repo)
    return node

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
