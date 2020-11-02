"""
python compare_core_metrics.py [path_to_unweighted_reference_core_json] [weighted_core1_json] [weighted_core2_json] [.....]
"""

# Following metrics will be tracked

# only for the 1st file
# sU - Total number of k-shells in the unweighted decomposition

# (one for each of the other files)
# sW - Total number of k-shells in the weighted decomposition
# NC - Number of common nodes in cores obtained from the two methods
# NUW - Fraction of the common nodes

import json
import sys
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.ticker as ticker
import os
import math

def compareCores(weightedCorePath, unweightedCorePath):
    weightedCoreFileHandl = open(weightedCorePath)
    weightedCores = json.loads(weightedCoreFileHandl.read())
    weightedCoreValues = set()
    for node in weightedCores:
        weightedCoreValues.add(weightedCores[node])
    
    unweightedCoreFileHandl = open(unweightedCorePath)
    unweightedCores = json.loads(unweightedCoreFileHandl.read())
    unweightedCoreValues = set()
    for node in unweightedCores:
        unweightedCoreValues.add(unweightedCores[node])

    # calculate the number of nodes that have the same core number
    commonCores = 0
    for node in unweightedCores:
        if unweightedCores[node] == weightedCores[node]:
            commonCores += 1

    weightedFractionCorrect = commonCores / len(weightedCores.keys())

    print("____________________________________________________________")
    print(weightedCorePath)
    print("Weighted core count: "+str(len(weightedCoreValues)))
    print("Weighted core min: "+str(min(list(weightedCoreValues))))
    print("Weighted core max: "+str(max(list(weightedCoreValues))))

    print("UnWeighted core count: "+str(len(unweightedCoreValues)))
    print("UnWeighted core min: "+str(min(list(unweightedCoreValues))))
    print("UnWeighted core max: "+str(max(list(unweightedCoreValues))))

    print("Common Cores: "+str(commonCores))
    print("Fraction Common: "+str(weightedFractionCorrect))
    print("____________________________________________________________")


unweighted_ref_file_path = sys.argv[1]
weighted_core_files_path = []
for i in range(2, len(sys.argv)):
    weighted_core_files_path.append(sys.argv[i])

if len(weighted_core_files_path) == 0:
    print("Add some weighted core file paths")
    exit()

for weighted_core_file in weighted_core_files_path:
    compareCores(weighted_core_file, unweighted_ref_file_path)
