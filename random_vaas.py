
import igraph as ig
from mealpy.swarm_based import PSO
from mealpy.utils.space import FloatVar, IntegerVar
from network_smart.local_paths import *

from network_smart.vass import VaaS
import numpy as np
from composition.CP_PSO_VaaS import PSO_VaaS
from network_smart.region import Region
from network_smart.network_region import *
from composition.composite_vaas import composite_vaas

import pandas as pd
from main import create_regions


def run_random(regions, user_query, vaas_set, weights):
    

    # Define the bounds for your optimization problem using FloatVar
    #bounds = IntegerVar(lb=0, ub=m - 1, name="taxi_index")
    
    c = local_paths(regions)
    regions_path = c.run(user_query["source"], user_query["destination"])  
    
    #list_of_local_paths = {'path': 1, 'regions': {0, 1, 3}, 'paths': [{'uid': 0, 'nodes': [0, 1, 9], 'weight': 111.20748446026197}, {'uid': 1, 'nodes': [9, 28, 20], 'weight': 108.66811158549974}]}
    # Run PSO to select vaas for regions: 
    # I will use "Employee Rostering Problem Using Woa Optimizer: https://github.com/thieu1995/mealpy/tree/master
    
    # Extract  regions to be our path:
    traversed_region = regions_path['regions']
    solution= []
    for r in traversed_region:
        vaas = random.choice(range(len(vaas_set)))
        solution.append(vaas)
        
    bounds = IntegerVar(lb=[0, ]*len(traversed_region), ub=[len(vaas_set)-1, ]*len(traversed_region), name="vaas_var")

    problem = composite_vaas(path_regions=regions_path, weights=weights,query=user_query, set_vaas=vaas_set, bounds=bounds)
    print(problem.obj_func(solution))
    

if __name__ == '__main__':
    regions = create_regions(number_region=2, min_edges=2, min_nodes=20, max_edges=15, max_nodes=30)
    user_query ={'source': 1,'destination':30, 'QoS':{'cost': 8, 'speed':100, 'availability':0.98, 'reputation': 0.8, 'place':2, 'rating':8}}
    vaas_dataset = pd.read_csv("./dataset/vaas.csv")["name_dataset"]
   
    for d in vaas_dataset:
        # proceed each dataset 
        vaas = pd.read_csv(f"./dataset/vaas/{d}.csv")
        vaas_set =[]
        for  index, v in vaas.iterrows():
            vs = VaaS(data=v)
            vaas_set.append(vs)
    run_random(regions, user_query, vaas_set, [0.25, 0.25, 0.25, 0.25])
    """
    problem = {
        "obj_func": fitness_function,  # Your fitness function defined elsewhere
        "bounds": bounds,  # Use FloatVar for continuous optimization
        "minmax": "min",  # Minimize the fitness function
        "verbose": True
    }
    
    # Create PSO instance and solve
    pso = PSO.OriginalPSO(epoch=100, pop_size=50)
    best_solution, best_fitness = pso.solve(problem)

    # Extracting additional details from the best solution
    best_path = best_solution[0]
    selected_taxis = best_solution[1]

    # Calculate details for best solution
    availability, cost, rating = fitness_function(best_solution)[1:]

    print(f"Best path: {best_path}, Selected taxis: {selected_taxis}")
    print(f"Best fitness: {best_fitness}, Total availability: {availability}, Total cost: {cost}, Average rating: {rating}")
"""