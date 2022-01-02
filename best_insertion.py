from math import sqrt, inf
import matplotlib.pyplot as plt
import csv, random, copy

def BestInsertion(V,C):
    # Initialize state of nodes, W of Hamiltonian path, Nodes of Hamiltonian path and queue of nodes
    S = ['N'] * len(V)
    W = 0
    Q = []
    V_copy = copy.copy(V)
    # Choose 3 random nodes from queue of nodes as list
    start = random.sample(range(len(V_copy)),3)
    # Set 3 starting nodes as Open
    for i in range(3):
        S[start[i]] = 'O'
        # Calculate distnce W of startig path
        if i+1 < 3:
            dist = sqrt((C[start[i]][0]-C[start[i+1]][0])**2 + (C[start[i]][1]-C[start[i+1]][1])**2)
            W = W + dist
        # In the last iteration return to the first node
        else:
            dist = sqrt((C[start[i]][0]-C[start[0]][0])**2 + (C[start[i]][1]-C[start[0]][1])**2)
            W = W + dist
        # remove visited nodes from queue
        V_copy.remove(start[i])
        # Add starting points to Hamiltonian path
        Q.append(start[i])
    
    # Until there is non-visited node:
    while 'N' in S:
        # Get random non-visited node
        u = random.choice(V_copy)
        # Initialize minimal extention of W
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
            # If between v1 u v2 is minimum, set it as minW ans mark place, where can be possibly added node to Hamiltonian path
            if new_dist < minW:
                minW = new_dist
                new_node = j+1
        # Set node u as open
        S[u] = 'O'
        # Insert node to Hamiltonian path
        Q.insert(new_node, u)
        # Remove added node form queue
        V_copy.remove(u)
        # Add minimum distance between v1 u v2 to W of Hamiltonian path
        W = W + minW
    # Close Hamiltonian path
    Q.append(Q[0])
    return Q, W

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
with open('data//coord_10000.csv','r') as f:
    reader = csv.reader(f,delimiter=';')
    for row in reader:
        V.append(int(row[0]))
        C[int(row[0])] = [float(row[1]),float(row[2])]

Q, W = BestInsertion(V,C)
print(W, Q)
plot(Q, C)