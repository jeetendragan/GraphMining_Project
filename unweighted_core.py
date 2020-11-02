"""
python core.py [path_to_graph_json] [output_directory] [name_of_graph]
"""

import json
import sys
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.ticker as ticker
import os
import numpy as np

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

cores = calculate_cores(graph)
outputJsonPath = os.path.join(sys.argv[2], sys.argv[3]+"_cores.json")
# Outputs core dict to json file
with open(outputJsonPath, 'w') as f:
    json.dump(cores, f)

fig, ax = plt.subplots(1,1)

# example title: ego-facebook core vector to stationary vector f1 scores
plt.figure(figsize=(20,10)).suptitle(sys.argv[3] + " core numbers" , y = 0.90)

nodes_per_core = {}
allCores = []
for node, core in cores.items():
    if core not in nodes_per_core:
        nodes_per_core[core] = 1
    else:
        nodes_per_core[core] += 1
    allCores.append(core)

x = []
y = []
for core, num_nodes in nodes_per_core.items():
    x.append(core)
    y.append(num_nodes)

#plt.plot(x, y, '.k')
#hist, bins = np.histogram(allCores, bins=50)
#plt.bar(allCores, bins)

plt.hist(allCores, bins=50)

#ax.xaxis.set_major_locator(ticker.MultipleLocator(500))
plt.xlabel('core number')
plt.ylabel('# of nodes')

outputImagePath = os.path.join(sys.argv[2], sys.argv[3]+"_cores_hist.png")
plt.savefig(outputImagePath)