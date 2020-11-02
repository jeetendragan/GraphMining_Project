"""
python weighted_core.py [path_to_graph_json] [path_to_weights_json] [name_of_graph]
"""

import ast
import json
import sys
from copy import deepcopy
import math
import statistics
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.ticker as ticker

# graph: {1: [neighbors of 1], 2: [neighbors of 2], ...}

def calculate_cores(graph):
    cores = {}
    for node in graph.keys():
        # initially the cores of each node will be the degree of the node
        cores[node] = len(graph[node])
    update_stop = False
    while not update_stop:
        update_stop = True
        for node in graph.keys(): # for each node in graph
            neighbor_cores = []
            for neighbor in graph[node]: # for each neighbour of node
                neighbor_cores.append(cores[neighbor]) # make a list of the cores of all neighbours
            neighbor_cores.sort() # sort the nieghbour core list
            h_index = neighbor_cores[0] # init
            values_left = len(neighbor_cores) # size of the list/num of neighbours
            if h_index > values_left: 
                h_index = values_left
            else:
                for idx in range(1, values_left):
                    if neighbor_cores[idx] > values_left - idx:
                        if values_left - idx > h_index:
                            h_index = values_left - idx
                        break
                    h_index = neighbor_cores[idx]
            if h_index != cores[node]:
                cores[node] = h_index
                update_stop = False
    return cores

with open(sys.argv[1], 'r') as f:
    graph = {int(node): neighbors for node, neighbors in json.load(f).items()}

with open(sys.argv[2], 'r') as f:
    weights = {ast.literal_eval(k): v for k, v in json.load(f).items()}

print("Number of nodes: " + str(len(graph)))
m = 0
for node, neighbors in graph.items():
    m += len(neighbors)
m = m/2
print("Number of edges: " + str(m))
maxDeg = 0
for node, neighbors in graph.items():
    if len(neighbors) > maxDeg:
        maxDeg = len(neighbors)
print("Max Degree: " + str(maxDeg))
maxWei = 0
for edge, weight in weights.items():
    if weight > maxWei:
        maxWei = weight
print("Max Weight: " + str(maxWei))
meanWeight = 0
minWeight = sys.maxsize
for edge, weight in weights.items():
    meanWeight += weight
    if weight < minWeight:
        minWeight = weight
meanWeight = meanWeight / m
print("Mean Weight: " + str(meanWeight))


alpha = 0
beta = 1
for edge, weight in weights.items():
    weights[edge] = 1
print("Weights after norm: ")

cores = core_decomposition(graph, weights, alpha, beta)

# Outputs cores.items() to json file
with open(sys.argv[3]+ '_cores.json', 'w') as f:
    json.dump(cores, f)

k_shells = []
for node, core in cores.items():
    if core not in k_shells:
        k_shells.append(core)
print("Number of k-cores: " + str(len(k_shells)))

nodes_per_core = {}

for node, core in cores.items():
    if core not in nodes_per_core:
        nodes_per_core[core] = 1
    else:
        nodes_per_core[core] += 1

x = []
y = []

for core, num_nodes in nodes_per_core.items():
    x.append(core)
    y.append(num_nodes)
    
plt.plot(x, y, '.k')
plt.xlabel('core number')
plt.ylabel('# of nodes')

plt.savefig(sys.argv[3] + '_cores.png')
#plt.show()
