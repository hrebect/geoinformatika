from math import sqrt, inf
import matplotlib.pyplot as plt
import csv

def nn(V,C,u):
    # Save strarting point, Initialize state of nodes, W of Hamiltonian path, Nodes of Hamiltonian path 
    start = u
    S = ['N'] * len(V)
    Q = []
    Q.append(u) 
    W = 0
    # Set starting point as open 
    S[u] = 'O'
    # Until there is non-visited node:
    while 'N' in S:
        # Initialize minimal extention of W
        minW = inf
        for v in V:
            # Get non-visited node as v
            if S[v] == 'N':
                # calculate distance between u and v
                dist = sqrt((C[u][0]-C[v][0])**2 + (C[u][1]-C[v][1])**2)
                # set new minimum distance
                if dist < minW:
                    minW = dist
                    nn = v        
        # add nearest node to Hamiltonian path
        Q.append(nn)
        # set nearest node as new u
        u = nn
        S[u] = 'O'
        # add distance between u and v to W of Hamiltonian path
        W = W + minW
    # Close Hamiltonian path
    dist_to_start = sqrt((C[u][0]-C[start][0])**2 + (C[u][1]-C[start][1])**2)
    Q.append(start)
    W = W + dist_to_start
    # return Hamiltonian path as Q and its weight as W
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
with open('data//coord_cernosice.csv','r') as f:
    reader = csv.reader(f,delimiter=';')
    for row in reader:
        V.append(int(row[0]))
        C[int(row[0])] = [float(row[1]),float(row[2])]

#set starting point
u = 0
Q, W = nn(V,C,u)
plot(Q, C)
print(W, Q)


