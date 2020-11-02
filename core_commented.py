"""
python core.py path_to_graph_json path_to_output_json name_of_graph

Example: python core.py facebook.json facebook_cores.json facebook


path_to_graph_json is obtained via running read_txt.py

Example: python read_txt.py facebook.txt facebook.json


graph file (aka facebook.txt) is obtained via any online database, for example:
https://snap.stanford.edu/data/ (more database websites can be found through reverse engineering citations)
"""

import json
import sys

# graph: {1: [neighbors of 1], 2: [neighbors of 2], ...}
def calculate_cores(graph):

    # Initializes the core number of each node to its degree
    cores = {}
    for node in graph.keys():
        cores[node] = len(graph[node])
    
    """ 
        The h-index process works like this:

        We define an iteration to be when h-index is applied to all nodes in the graph
        Let core_prev be the core numbers after the previous iteration
        Let core be the core numbers after the current iteration

        update_stop = True if core_prev = core else update_stop = False

        As a result, once core_prev = core, we have obtained our core numbers.
        If core_prev != core, then we have to do another iteration (aka h-index to all nodes in the graph)

    """
    update_stop = False
    while not update_stop:
        update_stop = True

        # Does h-index for all nodes in the graph
        for node in graph.keys():

            # Sorts the list
            neighbor_cores = []
            for neighbor in graph[node]:
                neighbor_cores.append(cores[neighbor])
            neighbor_cores.sort()

            # Initializes h-index to first element in list
            h_index = neighbor_cores[0]

            # If first element in list is greater than length of list, initialize h-index to length of list
            values_left = len(neighbor_cores)
            if h_index > values_left:
                h_index = values_left
            else:
                # Else, iterate through the list to find the point where the value > remaining length of list
                for idx in range(1, values_left):
                    if neighbor_cores[idx] > values_left - idx:
                        if values_left - idx > h_index:
                            h_index = values_left - idx
                        break
                    h_index = neighbor_cores[idx]
            if h_index != cores[node]:
                cores[node] = h_index

                # update_stop is set to False if a node has a different h-index result from the previous iteration
                update_stop = False
    return cores

# Reads the graph obtained from read_txt.py
with open(sys.argv[1], 'r') as f:
    graph = {int(node): neighbors for node, neighbors in json.load(f).items()}

cores = calculate_cores(graph)

# Outputs cores to JSON file
with open(sys.argv[2], 'w') as f:
    json.dump(cores, f)
