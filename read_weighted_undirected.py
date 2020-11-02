""" 
python read_txt.py [directory of text file] [output directory] [name of graph]

Converts txt file into graph
    - Text File
        # node  neighbor_node
            0         1
            1         2
"""

import sys
import json
import os

graph = {}
weights = {}

f = open(sys.argv[1], "r")

for line in f:
    line = line.strip()
    delim = ""
    if line[:1].isdigit():
        if delim == "":
            for char in line:
                if not char.isdigit():
                    delim = char
                    break
        nodes = line.split(delim)
        nodes = [i for i in nodes if i]
        nodes = list(map(int, nodes))
        if nodes[0] not in graph:
            graph[nodes[0]] = []
        if nodes[1] not in graph:
            graph[nodes[1]] = []
        if nodes[1] not in graph[nodes[0]]:
            graph[nodes[0]].append(nodes[1])
        if nodes[0] not in graph[nodes[1]]:
            graph[nodes[1]].append(nodes[0])
        if (min(nodes[0], nodes[1]), max(nodes[0], nodes[1])) not in weights:
            weights[min(nodes[0], nodes[1]), max(nodes[0], nodes[1])] = nodes[2]

# Outputs graph to json file
outputGraphFile = os.path.join(sys.argv[2], sys.argv[3]+".json")
with open(outputGraphFile, 'w') as f:
    json.dump(graph, f)

outputWeightsFile = os.path.join(sys.argv[2], sys.argv[3]+"_weights.json")
with open(outputWeightsFile, 'w') as f:
    json.dump({str(k): v for k, v in weights.items()}, f)
