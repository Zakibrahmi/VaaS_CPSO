from network_smart.vass import VaaS
import numpy as np
from composition.CP_PSO_VaaS import PSO_VaaS
from network_smart.region import Region
from network_smart.network_region import *
from network_smart.vass import VaaS
import pandas as pd

def create_regions(number_region, min_edges, min_nodes, max_edges, max_nodes ):
	"""This function generates a set of regions 
	
	Keyword arguments:
	 	numer_region: number of region to be created
		min_edges/min_nodes: the minimum number of edges/nodes that compose the graph of each region
	Return: set of connected regions. For simplicity, one node are shared between 2 regions
	"""
	regions =[]
	uid_from=0
	for i in range(number_region):
		num_nodes = VaaS.generate_random_normal(min_nodes, max_nodes)
		num_edges = VaaS.generate_random_normal(min_edges, max_edges)
		r= Region(name=str(i), numberNodes=int(num_nodes),numEdges=int(num_edges), uid_from=uid_from)
		uid_from = int(num_nodes)-1 # to easly connecting region
		
		regions.append(r)
	# Create link between regions
	for i in range(number_region):
		for j in range(i + 1, number_region):
			intersection = [value for value in regions[i].graph.vs["id"] if value in regions[j].graph.vs["id"]]
			regions[i].addlinkedRegion(regions[j], intersection)

	return regions


#vaas_set= VaaS.generate_random_vaas([0, 1, 2],['car', 'bus'], 21)
#vaaSSS = sorted(vaaSSS, key=lambda VaaS: VaaS.get_convered_regions(), reverse=True)

list_of_local_paths = {'path': 1, 'regions': {0, 1, 3}, 'paths': [{'uid': 0, 'nodes': [0, 1, 9], 'weight': 111.20748446026197}, {'uid': 1, 'nodes': [9, 28, 20], 'weight': 108.66811158549974}]}


user_query ={'source': 1,'destination':10, 'QoS':{'cost': 8, 'speed':100, 'availability':0.98, 'reputation': 0.8, 'place':2, 'rating':8}}
regions_set = create_regions(number_region=2, min_edges=2, min_nodes=20, max_edges=15, max_nodes=30)

# We will find compositions from regions_set while varying vaas 
# read all datasets. They are stored in "./dataset/vaas.csv file"

vaas_dataset = pd.read_csv("./dataset/vaas.csv")["name_dataset"]

for d in vaas_dataset:
	# proceed each dataset 
	vaas = pd.read_csv(f"./dataset/{d}.csv")
	vaas_set =[]
	for  index, v in vaas.iterrows():
		vs = VaaS(data=v)
		vaas_set.append(vs)

	v = PSO_VaaS([0.25, 0.25, 0.25, 0.25],vaas_set, user_query, regions_set)
	v.run(5, to_store_result=d)
	print(v.best_solution.to_print())
