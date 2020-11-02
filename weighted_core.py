"""
python weighted_core.py [path_to_graph_json] [path_to_weights_json] [output_directory] [name_of_graph]
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
import os

# graph: {1: [neighbors of 1], 2: [neighbors of 2], ...}

def core_decomposition(graph, weights, alpha, beta):
    cores = {}
    nodes = []
    for node, neighbors in graph.items():
        weights_sum = 0
        for neighbor in neighbors:
            weights_sum += weights[(min(node, neighbor), max(node, neighbor))]
        degree = len(neighbors)
        weights_sum = math.pow(degree, alpha) * math.pow(weights_sum, beta)
        root = alpha + beta
        cores[node] = int(weights_sum**(1/root))
        nodes.append(node)
    while len(nodes) > 0:
        min_node = -1
        min_core = sys.maxsize
        for node in nodes:
            if cores[node] < min_core:
                min_core = cores[node]
                min_node = node
        nodes.remove(min_node)
        for neighbor in graph[min_node]:
            if neighbor in nodes:
                if cores[neighbor] > min_core:
                    weights_sum = 0
                    degree = 0
                    for node in graph[neighbor]:
                        if node in nodes:
                            weights_sum += weights[(min(node, neighbor), max(node, neighbor))]
                            degree += 1
                    weights_sum = math.pow(degree, alpha) * math.pow(weights_sum, beta)
                    new_core = int(weights_sum**(1/root))
                    cores[neighbor] = max(new_core, min_core)
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

alpha = 1
beta = 1
for edge, weight in weights.items():
    normalization = weight / meanWeight
    weights[edge] = int(max(math.floor(normalization / minWeight), 1))
print("Weights after norm: ")

cores = core_decomposition(graph, weights, alpha, beta)

# Outputs cores.items() to json file
outputJsonPath = os.path.join(sys.argv[3], sys.argv[4]+"_cores.json")
with open(outputJsonPath, 'w') as f:
    json.dump(cores, f)

k_shells = []
for node, core in cores.items():
    if core not in k_shells:
        k_shells.append(core)
print("Number of k-cores: " + str(len(k_shells)))

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

"""for core, num_nodes in nodes_per_core.items():
    x.append(core)
    y.append(num_nodes)"""
    
#plt.plot(x, y, '.k')
plt.hist(allCores, bins=50)

#ax.xaxis.set_major_locator(ticker.MultipleLocator(500))
plt.xlabel('core number')
plt.ylabel('# of nodes')

outputFilePath = os.path.join(sys.argv[3], sys.argv[4]+"_cores.png")
plt.savefig(outputFilePath)