MAX_STEP = 100
ADJ_LIST = [[1,3,4],[0,2,4],[1,4,5],[0,4,6],[0,1,2,3,5,6,7,8],[2,4,8],[3,4,7],[4,6,8],[4,5,7]]

class Node:
    def __init__(self):
        self.parent = None
        self.state = None
        self.children = []
        self.value = None

    def dump(self, evaluated_nodes):
        print ""
        print self.state_key() + " -> " + str(self.value) + " : " + str(evaluated_nodes[self.state_key()])
        print "------- children ------"
        for n in self.children:
            print n.state_key() + " -> " + str(n.value) + " : " + str(evaluated_nodes[n.state_key()])
        print ""
        for n in self.children:
            n.dump(evaluated_nodes)

    def state_key(self):
        return ''.join(self.state)

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

    def is_time_to_move(self, min_or_max):
        a_count = 0
        b_count = 0
        for el in self.state:
            if(el == 'A'):
                a_count += 1
            if(el == 'B'):
                b_count += 1
        if(min_or_max == 0 and b_count >= 3):
            return True
        if(min_or_max == 1 and a_count >= 3):
            return True
        return False

    def current_cells(self, min_or_max):
        return [i for i, el in enumerate(self.state) if el == ('A' if min_or_max == 1 else 'B')]

    def empty_cells(self):
        return [i for i, el in enumerate(self.state) if el == '-']

    def put_somewhere(self, min_or_max):
        for i in self.empty_cells():
            node = Node()
            node.parent = self
            node.state = list(self.state)
            node.state[i] = 'A' if min_or_max == 1 else 'B'
            self.children.append(node)

    def move_somewhere(self, min_or_max):
        for i in self.current_cells(min_or_max):
            for j in ADJ_LIST[i]:
                if(self.state[j] != '-'):
                    continue
                node = Node()
                node.parent = self
                node.state = list(self.state)
                node.state[j] = 'A' if min_or_max == 1 else 'B'
                node.state[i] = '-'
                self.children.append(node)
                #print node.state


    def evaluate(self, min_or_max, step, evaluated_nodes):

        if(step == MAX_STEP):
            self.value = 0
            evaluated_nodes[self.state_key()] = self.value
            return 0

        if(min_or_max == 0 and self.is_over()):
            self.value = 3
            evaluated_nodes[self.state_key()] = self.value
            return 3

        if(min_or_max == 1 and self.is_over()):
            self.value = 0
            evaluated_nodes[self.state_key()] = self.value
            return -1

        if(self.state_key() in list(evaluated_nodes.keys())):
            return evaluated_nodes[self.state_key()]

        if(not self.is_time_to_move(min_or_max)):
            self.put_somewhere(min_or_max)
        else:
            self.move_somewhere(min_or_max)

        arr = []
        for el in self.children:
            arr.append(el.evaluate(1 - min_or_max, step+1, evaluated_nodes))

        if(min_or_max == 1):
            self.value = max(arr)
        else:
            self.value = min(arr)
        #print "current state:  " + self.state_key()
        #print "value:  " + str(self.value)
        evaluated_nodes[self.state_key()] = self.value
        return self.value

def build_tree():
    evaluated_nodes = {}
    node = Node()
    node.state = ['-','-','-','-','-','-','-','-','-']
    node.evaluate(1,0, evaluated_nodes)
    #print evaluted_nodes
    return node, evaluated_nodes

node, evaluated_nodes = build_tree()
node.dump(evaluated_nodes)
