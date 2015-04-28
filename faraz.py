#Max->1 Min->2 Null->0

graph=[[1,3,4],[0,2,4],[1,4,5],[0,4,6],[0,1,2,3,5,6,7,8],[2,4,8],[3,4,7],[6,4,8],[4,5,7]]
seen={}

MAX_STEP=100

def to_str(state,Max,l):
    return str(state)+"_"+str(Max)+"_"+str(int(l/50))

def alpha_beta(state,l,Max):
    global MAX_STEP
    if finished(state): return (1-2*Max)/float(l),0
    if l==MAX_STEP: return 0,0
    seen[to_str(state,Max,l)]="None"
    if Max:
        alpha=-float('inf')
        best_ins="-1"
        for s,ins in successors(state,Max,l):
            if seen.has_key(to_str(s,1-Max,l)) and seen[to_str(s,1-Max,l)]!="None":
                temp=seen[to_str(s,1-Max,l)]
                if temp!="None":
                    if temp>=alpha:
                        alpha=temp
                        best_ins=ins
            else:
                try:
                    temp=alpha_beta(s,l+1,1-Max)[0]
                    if temp>=alpha:
                        alpha=temp
                        best_ins=ins
                except:
                    if 0>=alpha:
                        alpha=0
                        best_ins=ins
            #if alpha==float('inf'): break
            #if alpha>0: break
        seen[to_str(state,Max,l)]=alpha
        return alpha,best_ins
    else:
        beta=float('inf')
        best_ins="-1"
        for s,ins in successors(state,Max,l):
            if seen.has_key(to_str(s,1-Max,l)) and seen[to_str(s,1-Max,l)]!="None":
                temp=seen[to_str(s,1-Max,l)]
                if temp!="None":
                    if temp<=beta:
                        beta=temp
                        best_ins=ins
            else:
                try:
                    temp=alpha_beta(s,l+1,1-Max)[0]
                    if temp<=beta:
                        beta=temp
                        best_ins=ins
                except:
                    if 0<=beta:
                        beta=0
                        best_ins=ins
            #if beta==-float('inf'): break
            #if beta<0: break
        seen[to_str(state,Max,l)]=beta
        return beta,best_ins

def finished(state):
    for j in [0,1,2]:
        if sum([state[i]==state[i+1]!=0 for i in [0+3*j,1+3*j]])==2:
            return True
    for j in [0,1,2]:
        if sum([state[i]==state[i+3]!=0 for i in [0+j,3+j]])==2:
            return True
    return state[0]==state[4]==state[8]!=0 or state[2]==state[4]==state[6]!=0

def successors(state,Max,l):
    if(l<6):
        for i in [0,1,2,3,4,5,6,7,8]:
            if state[i]==0:
                cp=[x for x in state]
                cp[i]=2-Max
                yield cp,str(i)
    else:
        global graph
        for i in [0,1,2,3,4,5,6,7,8]:
            if state[i]==(2-Max):
                for j in graph[i]:
                    if state[j]==0:
                        cp=[x for x in state]
                        cp[i]=0
                        cp[j]=(2-Max)
                        yield cp,str(i)+str(j)


import sys
import socket 


# Constants
FREE_SIGN = '-'
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
my_step = int(MY_NUMBER)-1
game_state = agent_socket.recv(BUFFER_SIZE)
while game_state != GAME_OVER_MESSAGE:
    seen={}
    state=[0]*9
    for i,x in enumerate(game_state):
        if x!=FREE_SIGN: state[i]=(int(x)+int(MY_NUMBER)-1)
        else: state[i]=0
        if state[i]>2: state[i]-=2
    #print my_step
    result=alpha_beta(state,my_step,1)
    ins=result[1]
    print result,state
    agent_socket.send(str(ins))
    my_step += 2
    game_state = agent_socket.recv(BUFFER_SIZE)
agent_socket.close()

'''
state=[0]*9
state[3]=1
state[4]=2
state[5]=1
state[6]=2
state[7]=0
state[8]=2
#print [s for s in successors(state,1,)]
print alpha_beta(state,5,1)
print len(seen)
print u
'''
