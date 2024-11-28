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
from vaas_ffca import *
import time
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
        #print(subset)
        
        subsets.append(subset)  # Add the subset to the list of subsets
    return subsets

#vaaSSS = sorted(vaaSSS, key=lambda VaaS: VaaS.get_convered_regions(), reverse=True)
if __name__ == '__main__':
    
    set_datasets = [300, 600,900, 1200, 1500, 1800, 2100, 2400, 2700, 3000]
    user_query ={'source': 1,'destination':30, 'QoS':{'cost': 8, 'speed':100, 'availability':0.95, 'reputation': 0.8, 'place':2, 'rating':8}}
    regions =[10, 20, 30, 40, 50]
    functions =["all", "cost","availability", "reputation", "time"]
    weights = [0.25, 0.25, 0.25, 0.25]
    # Generate vaas Datasets 
    """
    regions = [i for i in range(50 + 1)]        
    facilities =['car', 'bus']
    VaaS.create_vaas_datasets(set_datasets, "./dataset/vaas2/", regions, facilities)
    """
    """
    for number_regions in [50]:      
        
        # Generate regions Datasets 
        regions_set = Region.create_regions(number_region=number_regions, min_edges=2, min_nodes=20, max_edges=15, max_nodes=30)
        
        # Scenario 1: Compute compositions from regions_set (20 regions) while varying vaas      
        # Read all datasets. They are stored in "./dataset/vaas.csv file"       
        #vaas_dataset = pd.read_csv("./dataset/vaas.csv")["name_dataset"]   
        functions =["all", "cost","availability", "reputation", "time"]
        c = local_paths(regions_set)
        regions_path = c.run(user_query["source"], user_query["destination"])      
        # Extract  regions to be our path:
        traversed_region = regions_path['regions']
        # Each function is executed on different datasets and different algo
        #for sheet
        
        data_dict = {f: [] for f in functions}
        for f in functions:
            data ={}  
            for d in set_datasets:
                
                # proceed each dataset 
                vaas = pd.read_csv(f"./dataset/vaas/vaas_{d}.csv")
                vaas_set =[]
                # Generate the set of Vass from the csv file
                for  index, v in vaas.iterrows():
                    vs = VaaS(data=v)
                    vaas_set.append(vs)
                bounds = IntegerVar(lb=[0, ]*len(traversed_region), ub=[len(vaas_set)-1, ]*len(traversed_region), name="vaas_var")
                problem = composite_vaas(bounds=bounds,path_regions=regions_path, weights=weights,query= user_query, set_vaas= vaas_set, objective_function=f)
                #data.update({"dataset":d})        
                # run the set of algorihm; we can use loop on the array of algo name.
                
                # I will do it manully 
                v = PSO_VaaS(weights=weights,set_vaaSs=vaas_set, user_query=user_query, regions= regions_set,function=f, k_worsts=1)
                start_time_CPSO = time.time()
               
                result = v.run(path_region=regions_path, iterations=100)
                time_CPSO = time.time() - start_time_CPSO
                #data.update({"CPSO":result})
                #PSO 
                start_time =time.time()
                res_pso= run_pso(problem=problem)
                time_pso = time.time()- start_time
                #data.update({"PSO":res_pso})
                # Ramdom
                random_result= run_random(traversed_region=traversed_region, problem=problem, vaas_set=vaas_set)
                #data.update({"random":random_result})
                #CRO 
                start_time_cro = time.time()
                res_cro = run_cro(problem=problem, regions=traversed_region, vaas_set=vaas_set)
                #data.update({"CRO":res_cro})
                time_cro = time.time() - start_time_cro
                # FCA
                start_time_fca = time.time()
                res_fca = run_ffca(vaas_set, traversed_region, problem)
                time_fca = time.time() -start_time_fca
                #data.update({"FCA":res_fca})
            
                data_dict[f].append({"dataset": d, 
                                      "FCA":time_fca,
                                      "CRO":time_cro,
                                      "PSO":time_pso,
                                      "CPSO":time_CPSO
                                     })
               
        # Create an Excel file with multiple sheets
        with pd.ExcelWriter(f"results/time_{number_regions}.xlsx") as writer:
             for f in functions:
               # Convert the data to a DataFrame
                df = pd.DataFrame(data_dict[f])                
                # Write the DataFrame to an Excel sheet
                df.to_excel(writer, sheet_name=f, index=False)
    
    """  
    # Scenario 2: vaas fix and varying  number of region    
    """
    for d in [3000]:  
        vaas = pd.read_csv(f"./dataset/vaas/vaas_{d}.csv")
        vaas_set =[]
        # Generate the set of Vass from the csv file
        for  index, v in vaas.iterrows():
            vs = VaaS(data=v)
            vaas_set.append(vs)     
    
        # Each function is executed on different datasets and different algo
        #for sheet
        data_dict = {f: [] for f in functions}
        for f in functions:
            
            data ={}  
            for r in regions:
                # Generate regions Datasets 
                regions_set = Region.create_regions(number_region=r, min_edges=2, min_nodes=20, max_edges=15, max_nodes=30)
                    
                c = local_paths(regions_set)
                regions_path = c.run(user_query["source"], user_query["destination"])      
                # Extract  regions to be our path:
                traversed_region = regions_path['regions']
                # proceed each dataset 
                
                bounds = IntegerVar(lb=[0, ]*len(traversed_region), ub=[len(vaas_set)-1, ]*len(traversed_region), name="vaas_var")
                problem = composite_vaas(bounds=bounds,path_regions=regions_path, weights=weights,query= user_query, set_vaas= vaas_set, objective_function=f)
                #data.update({"dataset":d})        
                # run the set of algorihm; we can use loop on the array of algo name.
                
                # I will do it manully 
                v = PSO_VaaS(weights=weights,set_vaaSs=vaas_set, user_query=user_query, regions= regions_set,function=f)
                
                result = v.run(path_region=regions_path, iterations=100)
                #data.update({"CPSO":result})
                #PSO 
                res_pso= run_pso(problem=problem)
                #data.update({"PSO":res_pso})
                # Ramdom
                random_result= run_random(traversed_region=traversed_region, problem=problem, vaas_set=vaas_set)
                #data.update({"random":random_result})
                #CRO 
                res_cro = run_cro(problem=problem, regions=traversed_region, vaas_set=vaas_set)
                #data.update({"CRO":res_cro})
                
                # FCA
                res_fca = run_ffca(vaas_set, traversed_region, problem)            
                data_dict[f].append({"regions": r, 
                                     "FCA":res_fca,
                                      "CRO":res_cro,
                                      "PSO":res_pso,
                                      "random":random_result,
                                      "CPSO":result
                                     })
               
        # Create an Excel file with multiple sheets
        with pd.ExcelWriter(f"results/fix_vaas_{d}.xlsx") as writer:
             for f in functions:
               # Convert the data to a DataFrame
                df = pd.DataFrame(data_dict[f])                
                # Write the DataFrame to an Excel sheet
                df.to_excel(writer, sheet_name=f, index=False)
    """
    """
    # Question 3: Impcat of adjustement function in our algo while varing number k of worsts vaas to be adjusted
    top_k =[2,4,6,8,10,12,14,16]
    
    vaas = pd.read_csv(f"./dataset/vaas/vaas_3000.csv")
    vaas_set =[]
    # Generate the set of Vass from the csv file
    for  index, v in vaas.iterrows():
        vs = VaaS(data=v)
        vaas_set.append(vs)
        # Generate regions Datasets 
    regions_set = Region.create_regions(number_region=50, min_edges=2, min_nodes=20, max_edges=15, max_nodes=30)
    c = local_paths(regions_set)
    regions_path = c.run(user_query["source"], user_query["destination"])      
    # Extract  regions to be our path:
    traversed_region = regions_path['regions']
    # Each function is executed on different datasets and different algo
    #for sheet
        
    data =[]            
                
    bounds = IntegerVar(lb=[0, ]*len(traversed_region), ub=[len(vaas_set)-1, ]*len(traversed_region), name="vaas_var")
    problem = composite_vaas(bounds=bounds,path_regions=regions_path, weights=weights,query= user_query, set_vaas= vaas_set, objective_function="all")
    #data.update({"dataset":d})        
    # run the set of algorihm; we can use loop on the array of algo name.
    for k in top_k:
        # I will do it manully 
        v = PSO_VaaS(weights=weights,set_vaaSs=vaas_set, user_query=user_query, regions= regions_set,function="all", k_worsts=k)
        start_time_CPSO = time.time()
        
        result = v.run(path_region=regions_path, iterations=100)
        time_CPSO = time.time() - start_time_CPSO
        #data.update({"CPSO":result})
    
        data.append({"k_worst": k, 
                     "fintness":result                              
                    })
    df = pd.DataFrame(data)         
    # Create an Excel file with multiple sheets
    with pd.ExcelWriter(f"results/k_worsts.xlsx") as writer:                     
        # Write the DataFrame to an Excel sheet
        df.to_excel(writer, index=False)
    """
    """
    # Question 4:  Impact of R_st Or the lenght of request 
    # An possible solution: get path of each region R using R.getbestPath(self, source, destination) 
    vaas = pd.read_csv(f"./dataset/vaas/vaas_1200.csv")
    vaas_set =[]
    for  index, v in vaas.iterrows():
        vs = VaaS(data=v)
        vaas_set.append(vs)
    regions_set = Region.create_regions(number_region=21, min_edges=2, min_nodes=20, max_edges=15, max_nodes=30)
    
    # Create the set of request   
    
    source_node = regions_set[0].graph.vs['id'][0]
    data =[]  
    R =[12, 14, 16, 18, 20]
    f= "all"
    for k in R:

        destination_node =  regions_set[k-1].graph.vs['id'][-1] #latest node of the region
        user_query ={'source':  source_node,'destination':destination_node, 'QoS':{'cost': 8, 'speed':100, 'availability':0.95, 'reputation': 0.8, 'place':2, 'rating':8}}
        
        c = local_paths(regions_set)
        regions_path = c.run(user_query["source"], user_query["destination"]) 

        # Extract  regions to be our path:
        traversed_region = regions_path['regions']
        bounds = IntegerVar(lb=[0, ]*len(traversed_region), ub=[len(vaas_set)-1, ]*len(traversed_region), name="vaas_var")
        problem = composite_vaas(bounds=bounds,path_regions=regions_path, weights=weights,query= user_query, set_vaas= vaas_set, objective_function="all")
          
        #data.update({"CPSO":result})
        v = PSO_VaaS(weights=weights,set_vaaSs=vaas_set, user_query=user_query, regions= regions_set,function=f)
                
        result = v.run(path_region=regions_path, iterations=100)
        #data.update({"CPSO":result})
        #PSO 
        res_pso= run_pso(problem=problem)
        #data.update({"PSO":res_pso})
        # Ramdom
        random_result= run_random(traversed_region=traversed_region, problem=problem, vaas_set=vaas_set)
        #data.update({"random":random_result})
        #CRO 
        #res_cro = run_cro(problem=problem, regions=traversed_region, vaas_set=vaas_set, iterations=100)
        #data.update({"CRO":res_cro})
        
        # FCA
        res_fca = run_ffca(vaas_set, traversed_region, problem)            
        data.append({"R_st": k, 
                    "FCA":res_fca,
                    #"CRO":res_cro,
                    "PSO":res_pso,
                    "random":random_result,
                    "CPSO":result
                    })
        print(data)
    df = pd.DataFrame(data)         
    # Create an Excel file with multiple sheets
    with pd.ExcelWriter(f"results/R_st.xlsx") as writer:                     
        # Write the DataFrame to an Excel sheet
        df.to_excel(writer, index=False)
    """
    # Question 5:  Impact of the stopping criteria
    
    vaas = pd.read_csv(f"./dataset/vaas/vaas_1200.csv")
    vaas_set =[]
    for  index, v in vaas.iterrows():
        vs = VaaS(data=v)
        vaas_set.append(vs)
    regions_set = Region.create_regions(number_region=10, min_edges=2, min_nodes=20, max_edges=15, max_nodes=30)
    source_node = regions_set[0].graph.vs['id'][0]
    # Create the set of request   
    
    data =[]  
    stop_criteria =[100, 200, 300, 400, 500, 600, 700 , 800, 900, 100 ]
    f= "all"

    destination_node =  regions_set[4].graph.vs['id'][-1] #latest node of the region
    user_query ={'source':  source_node,'destination':destination_node, 'QoS':{'cost': 8, 'speed':100, 'availability':0.95, 'reputation': 0.8, 'place':2, 'rating':8}}
        
    c = local_paths(regions_set)
    regions_path = c.run(user_query["source"], user_query["destination"]) 

    # Extract  regions to be our path:
    traversed_region = regions_path['regions']
    bounds = IntegerVar(lb=[0, ]*len(traversed_region), ub=[len(vaas_set)-1, ]*len(traversed_region), name="vaas_var")
    problem = composite_vaas(bounds=bounds,path_regions=regions_path, weights=weights,query= user_query, set_vaas= vaas_set, objective_function="all")
   
    for k in stop_criteria:        
          
        #data.update({"CPSO":result})
        v = PSO_VaaS(weights=weights,set_vaaSs=vaas_set, user_query=user_query, regions= regions_set,function=f)
        start_time_CPSO = time.time()
        result = v.run(path_region=regions_path, iterations=k)
        time_CPSO = time.time() - start_time_CPSO

        #PSO 
        start_time_PSO = time.time()
        res_pso= run_pso(problem=problem, iteration=k)
        time_PSO = time.time() - start_time_PSO
        #data.update({"PSO":res_pso})
        #CRO 
        start_time_CRO = time.time()
        #res_cro = run_cro(problem=problem, regions=traversed_region, vaas_set=vaas_set, iteration=k)
        # time_CRO = time.time() - start_time_CRO

        data.append({"R_st": k, 
                    #"CRO":res_cro,
                    "PSO":res_pso,
                    "CPSO":result,
                    "time_CPSO": time_CPSO,
                    "time_PSO": time_PSO,
                    #"time_CRO":time_CRO
                    })
        print(data)
    df = pd.DataFrame(data)         
    # Create an Excel file with multiple sheets
    with pd.ExcelWriter(f"results/stop_creteria.xlsx") as writer:                     
        # Write the DataFrame to an Excel sheet
        df.to_excel(writer, index=False)
    