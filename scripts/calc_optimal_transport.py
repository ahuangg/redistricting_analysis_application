import matplotlib.pyplot as plt
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain,
                        proposals, updaters, constraints, accept, Election)
import os
import json
from networkx.readwrite import json_graph
from tqdm import tqdm
from OFFICIAL_OptimalTransport import *
import pickle
import numpy

'''
Import generated district plans as partitions
'''
partition_list = []

graph = Graph.from_json("./PA_VTDs.json")
my_updaters = {"population": updaters.Tally("TOTPOP", alias="population")}

dps_directory = './assignment_pickles'
for filename in os.listdir(dps_directory):
  file_path = os.path.join(dps_directory, filename)
  with open(file_path, "rb") as f:
    cur_assignment = pickle.load(f)
  cur_partition = GeographicPartition(graph, assignment=cur_assignment, updaters=my_updaters)
  partition_list.append(cur_partition)

distances = np.zeros((len(partition_list), len(partition_list)))

'''
Calculate distances using optimal transport
'''
print("Started calculating optimal transport")
for outer_idx, outer_plan in tqdm(enumerate(partition_list)):
  for inner_idx in range(outer_idx+1,len(partition_list)):
    inner_plan = partition_list[inner_idx]
    print(f"\nAt outer idx {outer_idx} and inner idx {inner_idx}")
    distances[outer_idx, inner_idx] = Pair(outer_plan,inner_plan).distance

print("Optimal transport distances:")
print(distances)

'''
Symmetrize the distance matrix (make it same across diagonals)
'''
import numpy as np

# distances = np.array([[ 0,69.2990957,  62.07662283, 31.74739153, 40.29863474],
#  [ 0,          0,         66.45427233, 81.13265257, 66.36285143],
#  [ 0,          0,          0,         79.092949,   38.55768295],
#  [ 0,          0,          0,          0,         62.92170143],
#  [ 0,          0,          0,          0,          0        ]])
distances = distances + distances.T - np.diag(distances.diagonal())
print("Symmetrized distances:")
print(distances)

'''
Perform Multidimensional Scaling (MDS)
'''
from sklearn.manifold import MDS

mds = MDS(n_components=2, random_state=0, dissimilarity='precomputed')
pos = mds.fit(distances).embedding_
print("Result:")
print(pos)




