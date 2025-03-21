import numpy as np
from mealpy.optimizer import Optimizer
from mealpy.utils.agent import Agent
from network_smart.local_paths import *
from typing import List, Union, Tuple, Dict
from mealpy.utils.agent import Agent
from mealpy.utils.problem import Problem
from math import gamma
from mealpy.utils.history import History
from mealpy.utils.target import Target
from mealpy.utils.termination import Termination
from mealpy.utils.logger import Logger
from mealpy.utils.validator import Validator
import concurrent.futures as parallel
from functools import partial

from composition.composite_vaas import composite_vaas
from utils.util import *
import copy
from network_smart.vass import VaaS
#from utils.util import generateRandomVector

class PSO_VaaS():

    def __init__(self, weights: List[float], set_vaaSs:List[VaaS], user_query=None, regions=None, function="all", k_worsts=1) -> None:
        self.weights = weights
        self.unused_vaass =set()
        self.set_vaaSs  = set_vaaSs        
        self.user_query= user_query # query ={"source", "destination", "QoS":{"cost", "availability", "time", "reputation", "rating", "places"}}
        self.all_solutions =[] # Array of composition
        self.regions = regions
        self.best_solution=None
        self.functionF = function
        self.topk_worsts=k_worsts
        print(self.topk_worsts)

    def candidate_CVaaS(self, list_of_local_paths):
        L_cp =[]
        L_cp_dic =[]
        L_ind =[]
        Vaas_tmp = self.set_vaaSs.copy()
        # Decreasing sorting of VaaSs in T based on the number of covered regions
        Vaas_tmp = sorted(Vaas_tmp, key=lambda VaaS: VaaS.get_convered_regions(), reverse=True)
        # Check if source and target stations belong to the same region; one region exist 
        if len(list_of_local_paths['regions']) ==1:            
            L_temp = [v for v in  Vaas_tmp if list(list_of_local_paths['regions'])[0] in v.covred_regions()]            
            L_cp = [[i] for i in L_temp]
            for c in L_temp:
                L_cp_dic.append([{'vaas':c, "regions": list(list_of_local_paths['regions'])}])           
            
        # Case 2: source and destiation reside in two connected regions (|Rst| = 2)
        elif len(list_of_local_paths['regions']) ==2:
            # Check if there exist a VaaS that covers these 2 regions            
            L_temp =  [v for v in  Vaas_tmp if set(list_of_local_paths['regions']).issubset(v.covred_regions())]
            
            if len(L_temp) >= 1:
                L_cp = [[i] for i in L_temp]
                for c in L_temp:                    
                    L_cp_dic.append([{'vaas':c, "regions": list(list_of_local_paths['regions'])}])
                
            else: # There is no VaaS can cover the 2 regions
                region_source = [list(list_of_local_paths['regions'])[0]]
                region_target = [list(list_of_local_paths['regions'])[1]]                
                L_source =  [v for v in  Vaas_tmp if set(region_source).issubset(v.covred_regions())]
                L_target =  [v for v in  Vaas_tmp if set(region_target).issubset(v.covred_regions())]                 
                L_cp = (list(zip(L_source, L_target))) # array of Tuple 
                cp_dic=[]
                for tuple in L_cp:
                    cp_dic.append({'vaas':tuple[0], "regions": region_source}) 
                    cp_dic.append({'vaas':tuple[1], "regions": region_target})
                L_cp_dic.append(cp_dic) 
        #Case 3: Source and destiation reside in two non-connected regions
        else: 
            ok =True            
            while ok :
                    R_temp = list_of_local_paths['regions'].copy()            
                    cp =[]
                    cp_dic=[]
                    i = 1                    
                    while len(R_temp) !=0:                        
                        # select the set of VaaS that cover the max regions in the path
                        #1. select VaaSs that  cover the first region in R_temp
                        cover_first_region = [v for v in Vaas_tmp if list(R_temp)[0] in v.covred_regions()]                        
                        if len(cover_first_region)>0:                            
                            #2. sorted the  set of cover_first_region according to the number of covred regions
                            tmp = sorted(cover_first_region, key=lambda VaaS: len(set(R_temp).intersection(VaaS.covred_regions())), reverse=True)
                            vass_covred_max = tmp[0]                             
                            Vaas_tmp.remove(vass_covred_max)
                            intersection_region = list(set(R_temp).intersection(vass_covred_max.covred_regions()))                            
                            cp.append(vass_covred_max)
                            vaas_dictionary ={'vaas':vass_covred_max, "regions": intersection_region}
                            #vaas_dictionary ={vass_covred_max: intersection_region}
                            cp_dic.append(vaas_dictionary)
                            for r in intersection_region:
                                R_temp.remove(r)
                        else:
                            i+=1
                        # All region are traversed without finding any VaaS can cover regions
                        if i == len(list_of_local_paths['regions']):
                               break   
                            
                    if i == len(list_of_local_paths['regions']):                        
                        ok = False                          
                    L_cp.append(cp)
                    L_cp_dic.append(cp_dic)        
        # Remove composition that doesn't covers all region of the path
        tmp_cl = L_cp_dic.copy()
       
        L_cp = list(np.hstack(L_cp))
        
        for cp in tmp_cl:            
            if self.check_feasible(cp, list_of_local_paths['regions'])== False:                
                L_cp_dic.remove(cp)
                L_cp.remove(cp[0]["vaas"])          

        # unused vaas     
        for v in self.set_vaaSs:
            if self.contains_id(L_cp, v.uid) == False:
                self.unused_vaass.add(v)    
        return L_cp_dic, self.unused_vaass

    def cVaaS_adjustment(self, composition_Vaas, k_worsts=1):
        """ replacing the worst VaaS representative with a fitter one
        arguments:
            composition_Vaas: a composition to be adjusted
        Return: adjusted composition, and the worst vaas of this composition
        """
        fitness_tmp = {}        
        for vaas in composition_Vaas:
            f = vaas["vaas"].fitness            
            # to evaluate the worstness of a vaas we multply it's fitness by the violated of QoS (place, rating)
            fitness_tmp.update({vaas["vaas"]:f*vaas["vaas"].violation(self.user_query['QoS'])}) 
        # sorted the dictionary of <vaas, vaas_fitness*number_violation>
        # the higher the vaas_fitness*number_violation is, the vaas in the more affecting the global fitness => vaas is the worest
        if k_worsts > len(fitness_tmp):
            k_worsts = len(fitness_tmp)
        sorted_vaas = dict(sorted(fitness_tmp.items(), key=lambda x:x[1], reverse=True)[:k_worsts]) 
        worst_vaas=None
        
        # we can loop here to extract the top-k worset vaas
        for item in sorted_vaas.items():
            worst_vaas = item[0]
            # How to substitute the worst vaaS, in this version, with a another vaas that cover the same regions covred by the worst 
            substitors = [v for v in self.unused_vaass if (set(worst_vaas.covered_regions).issubset(v.covered_regions) or set(v.covered_regions).issubset(worst_vaas.covered_regions) )]     
            tmp = composition_Vaas.copy()                        
            if len(substitors)>0:                            
                #2. sorted the  set of cover_first_region according to the number of covred regions
                index=0
                tmp = composition_Vaas.copy()
                for vaas in composition_Vaas:
                    if vaas["vaas"] == worst_vaas:
                        break
                    else:
                        index+=1            
                tmp[index]["vaas"] = substitors[0]  
                #print(composition_Vaas)
                self.unused_vaass.add(worst_vaas)
             
        else: # it's not possible de sustituate the worst vaas 
            pass
        
        return tmp, worst_vaas     
   
    def check_feasible(self, composition, regions):
        # Check if a compositon is feasible 
        # identify the set of regions convered by the composition
        listtmp=[]
       
        if isinstance(composition, dict):
            listtmp = composition["regions"]           
        else: 
            for item in composition:
                listtmp+= item["regions"]  
        ar1 = np.array(listtmp)
        ar2 = np.array(list(regions))
        # check if all regions are coverd by list        
        return np.array_equal(ar1,ar2)    
   
    def contains_id(self, objects, search_id):
        """check if uid object exist in a list of object        
        Return: True of False
        """ 
        return any(obj.uid == search_id for obj in objects)
    
    def run(self, path_region, iterations=50):
        """The main program         
        Keyword arguments:
        argument -- description
        Return: return_description
        """
         
        #2. generate intiale solutions using candidate_CVaaS function
        compositions, unused = self.candidate_CVaaS(path_region)
        # Intialize Best solution
        self.best_solution = composite_vaas(path_regions=path_region, weights=self.weights,query=self.user_query, set_vaas=self.set_vaaSs, composite_solution=compositions[0], objective_function=self.functionF)
        self.best_solution.obj_func() 
        fitness = 0
        for c in compositions:
            self.all_solutions.append(composite_vaas(path_regions=path_region, weights=self.weights,query=self.user_query, set_vaas=self.set_vaaSs, composite_solution=c, objective_function=self.functionF))  
        #data =[["best_fintess", "cost", "availability", "reputation", "time"]]                 
        for it in range(0, iterations):          
            for sol in self.all_solutions:               
                # Evaluaiton
                fitness= sol.obj_func() 
                # Update best solution
                if sol.compare(self.best_solution):
                    self.best_solution = copy.deepcopy(sol)
                #print(self.best_solution.fitnes)
                    
                 # Ajustement
                adjusted, worst = self.cVaaS_adjustment(sol.solution, self.topk_worsts)
                sol.solution = adjusted
                sol.update_worst_vaas(worst)
            fitness= self.best_solution.obj_func() 
            
        return fitness         

    
    




                

        
            


