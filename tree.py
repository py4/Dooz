import sys
import random

MAX_STEP = 100
ADJ_LIST = [[1,3,4],[0,2,4],[1,4,5],[0,4,6],[0,1,2,3,5,6,7,8],[2,4,8],[3,4,7],[4,6,8],[4,5,7]]

def pretty_show(state):
    print ""
    print state[0] + " " + state[1] + " " + state[2]
    print state[3] + " " + state[4] + " " + state[5]
    print state[6] + " " + state[7] + " " + state[8]
    print ""


class Node:
    def __init__(self):
        self.parent = None
        self.state = None
        self.children = []
        self.value = None

    def dump(self, evaluated_nodes, min_or_max):
        print ""
        print self.state_key(min_or_max) + " -> " + str(self.value) + " : " + str(evaluated_nodes[self.state_key(min_or_max)])
        print "------- children ------"
        for n in self.children:
            print n.state_key(1 - min_or_max) + " -> " + str(n.value) + " : " + str(evaluated_nodes[n.state_key(1 - min_or_max)])
        print ""
        for n in self.children:
            n.dump(evaluated_nodes, 1-min_or_max)

    def state_key(self, min_or_max):
        self.state = map(str, self.state)
        return ''.join(self.state)+str(min_or_max)

    def count_h2(self, char):
        c = 0
        for i in range(0,3):
            arr = [self.state[i], self.state[i+3], self.state[i+6]]
            if(arr.count(char) > 1):
                c += arr.count(char) - 1
        for i in [0,3,6]:
            arr = [self.state[i], self.state[i+1], self.state[i+2]]
            if(arr.count(char) > 1):
                c += arr.count(char) - 1
        arr = [self.state[0], self.state[4], self.state[8]]
        if(arr.count(char) > 1):
            c += arr.count(char) - 1
        arr = [self.state[2], self.state[4], self.state[6]]
        if(arr.count(char) > 1):
            c += arr.count(char) - 1
        return c

    def count_h(self, char):
        count = 0
        for i in range(0,3):
            if(self.state[i]==self.state[i+6]==char and self.state[i+3] =='-'):
                count += 1
        for i in [0,3,6]:
            if(self.state[i] == self.state[i+2] == char and self.state[i+1] == '-'):
                count += 1
        if(self.state[0] == self.state[8] == char and self.state[4] == '-'):
            count += 1
        if(self.state[2] == self.state[6] == char and self.state[4] == '-'):
            count += 1
        return count

    def get_h(self, me, he):
        return self.count_h(me) - self.count_h(he)

    def is_over(self):
        if ((self.state[0] == self.state[1] == self.state[2] != '-') or \
	    (self.state[3] == self.state[4] == self.state[5] != '-') or \
	    (self.state[6] == self.state[7] == self.state[8] != '-') or \
	    (self.state[0] == self.state[3] == self.state[6] != '-') or \
	    (self.state[1] == self.state[4] == self.state[7] != '-') or \
	    (self.state[2] == self.state[5] == self.state[8] != '-') or \
	    (self.state[0] == self.state[4] == self.state[8] != '-') or \
	    (self.state[2] == self.state[4] == self.state[6] != '-')):
            return True
        return False

    def is_time_to_move(self, min_or_max, me, he):
        me_count = 0
        he_count = 0
        for el in self.state:
            if(el == me): me_count += 1
            if(el == he): he_count += 1
        if(min_or_max == 0 and he_count >= 3):
            return True
        if(min_or_max == 1 and me_count >= 3):
            return True
        return False

    def current_cells(self, min_or_max, me, he):
        return [i for i, el in enumerate(self.state) if el == (me if min_or_max == 1 else he)]

    def empty_cells(self):
        return [i for i, el in enumerate(self.state) if el == '-']

    def put_somewhere(self, min_or_max, evaluated_nodes, me, he):
        for i in self.empty_cells():
            node = Node()
            node.parent = self
            node.state = list(self.state)
            node.state[i] = me if min_or_max == 1 else he
            if(node.state_key(1-min_or_max) in list(evaluated_nodes.keys())):
                node.value = evaluated_nodes[node.state_key(1-min_or_max)]
            self.children.append(node)

    def move_somewhere(self, min_or_max, evaluated_nodes, me, he):
        for i in self.current_cells(min_or_max, me, he):
            for j in ADJ_LIST[i]:
                if(self.state[j] != '-'):
                    continue

                node = Node()
                node.parent = self
                node.state = list(self.state)
                node.state[j] = me if min_or_max == 1 else he
                node.state[i] = '-'

                if(node.state_key(1-min_or_max) in list(evaluated_nodes.keys())):
                    node.value = evaluated_nodes[node.state_key(1-min_or_max)]
                self.children.append(node)


    def evaluate(self, min_or_max, step, evaluated_nodes, state_repository, me, he):

        if(step == MAX_STEP):
            if(evaluated_nodes.has_key(self.state_key(min_or_max))):
                if(evaluated_nodes[self.state_key(min_or_max)] != 0):
                    self.value = evaluated_nodes[self.state_key(min_or_max)]
                    return self.value
            else:
                #if(self.get_h(me,he) != 0):
                #    self.value = self.get_h(me, he)
                #    if(self.value > 3):
                #        self.value = 2.5
                #    if(self.value < -1):
                #        self.value = -0.5
                    #self.value = max(self.get_h(me, he)
                    #self.value = float(0.5) / (self.get_h(me, he))
                #else:
#                self.value = self.get_h(me, he)
                self.value = 0
                #evaluated_nodes[self.state_key(min_or_max)] = self.value
                return self.value

        if(min_or_max == 0 and self.is_over()):
            self.value = 3
            evaluated_nodes[self.state_key(min_or_max)] = self.value
            return 3

        if(min_or_max == 1 and self.is_over()):
            self.value = -1
            evaluated_nodes[self.state_key(min_or_max)] = self.value
            return -1

        if(evaluated_nodes.has_key(self.state_key(min_or_max))):
            return evaluated_nodes[self.state_key(min_or_max)]

        if(not self.is_time_to_move(min_or_max, me, he)):
            self.put_somewhere(min_or_max, evaluated_nodes, me, he)
        else:
            self.move_somewhere(min_or_max, evaluated_nodes, me, he)

        arr = []
        for el in self.children:
            value = el.evaluate(1-min_or_max, step+1, evaluated_nodes, state_repository, me, he)
            arr.append(value)

        if(min_or_max == 1):
            self.value = max(arr)
            index = arr.index(max(arr))
        else:
            self.value = min(arr)
            index = arr.index(min(arr))

        state_repository[self.state_key(min_or_max)] = self.children[index].state_key(1-min_or_max)
#        print self.state_key(min_or_max) + " -> " + self.children[index].state_key(1-min_or_max) + " : " + str(self.children[index].value)
        evaluated_nodes[self.state_key(min_or_max)] = self.value
        return self.value

def build_tree(initial_state, me, he):
    state_repository = {}
    evaluated_nodes = {}
    node = Node()
    node.state = initial_state[:]
    node.evaluate(1,0, evaluated_nodes, state_repository, me, he)
    return node, evaluated_nodes, state_repository

initial_state = ['-','-','-','-','-','-','-','-','-']

node, evaluated_nodes, state_repository = build_tree(initial_state, '1', '2')
