"""
python read_txt.py [directory of text file] [directory of json output file]

Converts txt file into graph
    - Text File
        # node  neighbor_node
            0         1
            1         2
"""

import sys
import json

graph = {}

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
        nodes = list(map(int, nodes))
        if nodes[0] not in graph:
            graph[nodes[0]] = []
        if nodes[1] not in graph:
            graph[nodes[1]] = []
        if nodes[1] not in graph[nodes[0]]:
            graph[nodes[0]].append(nodes[1])
        if nodes[0] not in graph[nodes[1]]:
            graph[nodes[1]].append(nodes[0])

# Outputs graph to json file
with open(sys.argv[2], 'w') as f:
    json.dump(graph, f)
