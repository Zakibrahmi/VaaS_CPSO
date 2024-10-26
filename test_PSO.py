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


import random

def generate_subsets(set_name_regions, n):
    selected_regions = set()  # To keep track of selected regions across all iterations
    subsets = []  # List to hold the n subsets

    for _ in range(n):
        subset = set()  # Use a set to ensure uniqueness

        # If there are regions that haven't been selected yet, select one of them
        if len(selected_regions) < len(set_name_regions):
            remaining_regions = list(set(set_name_regions) - selected_regions)
            chosen_region = random.choice(remaining_regions)
            subset.add(chosen_region)  # Add chosen region to the subset
            selected_regions.add(chosen_region)  # Mark as selected
        
        # Fill the rest of the subset by sampling from the entire set
        remaining_samples_needed = random.randint(1, len(set_name_regions) - len(subset))
        additional_samples = set(random.sample(set_name_regions, remaining_samples_needed))
        
        # Add the additional samples to the subset
        subset.update(additional_samples)
        print(subset)
        
        subsets.append(subset)  # Add the subset to the list of subsets
    return subsets



#vaaSSS = sorted(vaaSSS, key=lambda VaaS: VaaS.get_convered_regions(), reverse=True)
if __name__ == '__main__':
   
    # Generate vaas Datasets 
    number_regions= 2
    regions = [i for i in range(number_regions + 1)]
    set_datasets = [300, 600,900, 1200, 1500, 1800, 2100, 2400, 2700, 3000]
    facilities =['car', 'bus']
    #VaaS.create_vaas_datasets(set_datasets, "./dataset/vaas/", regions, facilities)
    user_query ={'source': 1,'destination':30, 'QoS':{'cost': 8, 'speed':100, 'availability':0.98, 'reputation': 0.8, 'place':2, 'rating':8}}
    
    # Generate regions Datasets 
    regions_set = create_regions(number_region=number_regions, min_edges=2, min_nodes=20, max_edges=15, max_nodes=30)
     
    # Scenario 1: Compute compositions from regions_set (20 regions) while varying vaas  
    
    # Read all datasets. They are stored in "./dataset/vaas.csv file"

    vaas_dataset = pd.read_csv("./dataset/vaas.csv")["name_dataset"]
   
    
    for d in vaas_dataset:
        # proceed each dataset 
        vaas = pd.read_csv(f"./dataset/vaas/{d}.csv")
        vaas_set =[]
        for  index, v in vaas.iterrows():
            vs = VaaS(data=v)
            vaas_set.append(vs)

        v = PSO_VaaS([0.25, 0.25, 0.25, 0.25],vaas_set, user_query, regions_set)
        v.run(5, to_store_result=d)
        print(v.best_solution.to_print())
    

    # Scenario 2: vaas fix and varying  number of region
    
    # Scenario 3: vaas and region fix and varying  lenght of request