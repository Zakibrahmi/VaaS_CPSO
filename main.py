from network_smart.vass import VaaS
import numpy as np
from composition.CP_PSO_VaaS import PSO_VaaS
from network_smart.region import Region
from network_smart.network_region import *

import pandas as pd
from pso_vaas import *
from random_vaas import *
import random
from cro import *

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
    regions_set = Region.create_regions(number_region=number_regions, min_edges=2, min_nodes=20, max_edges=15, max_nodes=30)
     
    # Scenario 1: Compute compositions from regions_set (20 regions) while varying vaas      
    # Read all datasets. They are stored in "./dataset/vaas.csv file"

    vaas_dataset = pd.read_csv("./dataset/vaas.csv")["name_dataset"]   
    functions =["all", "cost","availability", "reputation", "time"]

    c = local_paths(regions_set)
    regions_path = c.run(user_query["source"], user_query["destination"])      
    # Extract  regions to be our path:
    traversed_region = regions_path['regions']
    weights = [0.25, 0.25, 0.25, 0.25]
    # Each function is executed on different datasets and different algo
    dfs =[]
    sheet_names =[]
    result= "test"
    for f in functions:
        data ={}  
        for d in vaas_dataset:
            # proceed each dataset 
            vaas = pd.read_csv(f"./dataset/vaas/{d}.csv")
            vaas_set =[]
            # Generate the set of Vass from the csv file
            for  index, v in vaas.iterrows():
                vs = VaaS(data=v)
                vaas_set.append(vs)
            bounds = IntegerVar(lb=[0, ]*len(traversed_region), ub=[len(vaas_set)-1, ]*len(traversed_region), name="vaas_var")
            problem = composite_vaas(bounds=bounds,path_regions=regions_path, weights=weights,query= user_query, set_vaas= vaas_set, objective_function=f)
            data.update({"dataset":d})        
            # run the set of algorihm; we can use loop on the array of algo name.
            # I will do it manully 
            v = PSO_VaaS(weights=weights,set_vaaSs=vaas_set, user_query=user_query, regions= regions_set,function=f)
            result = v.run( path_region=regions_path, iterations=20)
            data.update({"CPSO":result})
            #PSO 
            res_pso= run_pso(problem=problem)
            data.update({"PSO":res_pso})
            # Ramdom
            random_result= run_random(traversed_region=traversed_region, problem=problem, vaas_set=vaas_set)
            data.update({"random":random_result})
            #CRO 
            res_cro = run_cro(problem=problem, regions=traversed_region, vaas_set=vaas_set)
            data.update({"CRO":res_cro})
               
        # Create a DataFrame
        #print(pd.DataFrame([data]))
        dfs.append(pd.DataFrame([data]))
        sheet_names.append(f)

    # Create an Excel file with multiple sheets
    with pd.ExcelWriter(f"results/result_{number_regions}.xlsx") as writer:
        for df, sheet_name in zip(dfs, sheet_names):
            df.to_excel(writer, sheet_name=sheet_name, index=False)
       
    # Scenario 2: vaas fix and varying  number of region
    
    # Scenario 3: vaas and region fix and varying  lenght of request
    
   
