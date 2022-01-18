from math import sqrt, inf
import matplotlib.pyplot as plt
import csv, random, copy

def rand(V):
    # initialize path with 3 random points
    start = random.sample(range(len(V)),3)
    return start

def nearest(V,C,u):
    # Initialize path with pount u and its 2 nearest neighbor
    start = []
    #Initialize state of nodes,
    S = ['N'] * len(V)
    start.append(u)
    # Set starting point as open 
    S[u] = 'O'
    # Finde 2 nearest neighbor
    for i in range(2):
        # Initialize minimal distance between points as inf
        minW = inf
        for v in V:
            # Get non-visited node as v
            if S[v] == 'N':
                # calculate distance between u and v
                dist = sqrt((C[u][0]-C[v][0])**2 + (C[u][1]-C[v][1])**2)
                # save minimum distance and nearest neighbor
                if dist < minW:
                    minW = dist
                    nn = v
        # Add nn to Initialize path          
        start.append(nn)
        S[nn] = 'O'
    return start

def extreme(C):
    # Initialize path as extreme points
    # get nodes with extreme coords
    minx = min(C.items(), key=lambda x: x[1][0])[0]
    miny = min(C.items(), key=lambda x: x[1][1])[0]
    maxx = max(C.items(), key=lambda x: x[1][0])[0]
    maxy = max(C.items(), key=lambda x: x[1][1])[0]
    # save extreme nodes in correct order
    start = [minx,maxy,maxx,miny]
    return start

def BestInsertion(V,C,a):
    # Input V = list of nodes, C = dictionary of coords of nodes, a = initialization method
    # Initialize state of nodes, W of Hamiltonian path, Nodes of Hamiltonian path and queue of nodes
    S = ['N'] * len(V)
    W = 0
    Q = []
    V_copy = copy.copy(V)
    # Initialize starting path by chosen method
    start = a
    #close initial Hamiltoninan path
    start.append(start[0])
    # Set 3 starting nodes as Open
    for i in range(len(start)-1):
        S[start[i]] = 'O'
        # Calculate distnce W of startig path
        dist = sqrt((C[start[i]][0]-C[start[i+1]][0])**2 + (C[start[i]][1]-C[start[i+1]][1])**2)
        W = W + dist
        # remove visited nodes from queue
        V_copy.remove(start[i])
        # Add starting points to Hamiltonian path
        Q.append(start[i])
    # Until there is non-visited node:
    while 'N' in S: 
        # Initialize minimal extention of W
        minW_all = inf
        # Search through all non-visited nodes
        for u in V_copy:
            # initialize minimal extention with this node
            minW = inf
            # Calculate distance between v1 u v2
            for j in range(len(Q)):
                v1 = Q[j]
                if j+1 < len(Q):
                    v2 = Q[j+1]
                else:
                    v2 = Q[0]
                # Distance (v1 u v2) - (v1 v2)
                new_dist = (sqrt((C[u][0]-C[v1][0])**2 + (C[u][1]-C[v1][1])**2) + sqrt((C[u][0]-C[v2][0])**2 + (C[u][1]-C[v2][1])**2) - sqrt((C[v1][0]-C[v2][0])**2 + (C[v1][1]-C[v2][1])**2))
                # If between v1 u v2 is minimum, set it as minW and mark place, where can be possibly added node to Hamiltonian path and which node can be possibly added
                if new_dist < minW:
                    minW = new_dist
                    position = j+1
            # If actual node u is best set u as minimum_node, save its best position and distance
            if minW < minW_all:
                minW_all = minW
                min_node = u
                position_best = position
        # Set node u as open
        S[min_node] = 'O'
        # Insert node to Hamiltonian path
        Q.insert(position_best, min_node)
        # Remove added node form queue
        V_copy.remove(min_node)
        # Add minimum distance between v1 u v2 to W of Hamiltonian path
        W = W + minW_all
    # Close Hamiltonian path
    Q.append(Q[0])
    return Q, W, start

def plot(Q,C):
    # Function to show Hamiltonian path
    x = []
    y = []
    for u in Q:
        x.append(C[u][0])
        y.append(C[u][1])
    plt.scatter(x, y)
    plt.plot(x, y)
    plt.show()

# Initialize data. Names of nodes as V (list), coordinates of V as C (dictionary)
V =[]
C = {}

# Load data from .csv 
with open('data//coord_cernosice.csv','r') as f:
    reader = csv.reader(f,delimiter=';')
    for row in reader:
        V.append(int(row[0]))
        C[int(row[0])] = [float(row[1]),float(row[2])]

Q, W, start = BestInsertion(V,C,nearest(V,C,20))
print(W, Q, start)
plot(Q, C)