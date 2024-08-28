import numpy as np
from mealpy.optimizer import Optimizer
from mealpy.utils.agent import Agent

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
import os
import time
import math
import random
from composite_Particles import composite_VaaS
from vass import VaaS
from utilFunctions import generateRandomVector

class PSO_VaaS():

    def __init__(self, weights: List[float], set_vaaSs:List[VaaS], user_query, iterations = 100) -> None:
        self.weights = weights
        self.unused_vaass =[]
        self.set_vaaSs  = set_vaaSs
        self.iterations = iterations
        self.user_query= user_query # query ={"source", "destination", "QoS":{"cost", "availability", "time", "reputation", "rating", "places"}}
    
    def candidate_CVaaS(self, list_of_local_paths):

        L_cp =[]
        L_cp_dic =[]
        L_ind =[]
        Vaas_tmp = self.set_VaaSs.copy()
        # Decreasing sorting of VaaSs in T based on the number of covered regions
        Vaas_tmp = sorted(Vaas_tmp, key=lambda VaaS: VaaS.get_convered_regions(), reverse=True)
        # check if Check if source and target stations belong to the same region; one region exist 
        if len(list_of_local_paths['regions']) ==1:
            
            L_cp = [v for v in  Vaas_tmp if list(list_of_local_paths['regions'])[0] in v.covered_regions]
            
            L_cp = [[i] for i in L_cp]
            for c in L_cp:
                L_cp_dic.append({'vaas':c, "regions": list(list_of_local_paths['regions'])})           
            
        # Case 2: source and destiation reside in two connected regions (|Rst| = 2)
        elif len(list_of_local_paths['regions']) ==2:
            # Check if there exist a VaaS that covers these 2 regions
            L_temp =  [v for v in  Vaas_tmp if set(list_of_local_paths['regions']).issubset(v.covered_regions)]
            #problem ici
            
            if len(L_temp) >= 1:
                L_cp = [[i] for i in L_temp]
                print(len(L_cp))
                for c in L_cp:                    
                    L_cp_dic.append({'vaas':c, "regions": list(list_of_local_paths['regions'])})

            else: # There is no VaaS can cover the 2 regions
                region_source = [list(list_of_local_paths['regions'])[0]]
                region_target = [list(list_of_local_paths['regions'])[1]]
                L_source =  [v for v in  Vaas_tmp if region_source in v.covered_regions]
                L_target =  [v for v in  Vaas_tmp if region_target in v.covered_regions]                 
                L_cp = (list(zip(L_source, L_target))) # array of Tuple 
                for tuple in L_cp:
                    L_cp_dic.append({'vaas':tuple[0], "regions": region_source}) 
                    L_cp_dic.append({'vaas':tuple[1], "regions": region_target})

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
                        cover_first_region = [v for v in Vaas_tmp if list(R_temp)[0] in v.covered_regions]
                        
                        if len(cover_first_region)>0:
                            
                            #2. sorted the  set of cover_first_region according to the number of covred regions
                            tmp = sorted(cover_first_region, key=lambda VaaS: len(set(R_temp).intersection(VaaS.covered_regions)), reverse=True)
                        
                            vass_covred_max = tmp[0]  
                            
                            Vaas_tmp.remove(vass_covred_max)
                            intersection_region = list(set(R_temp).intersection(vass_covred_max.covered_regions))
                            
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
        for v in self.set_VaaSs:
            if self.contains_id(L_cp, v.uid) == False:
                self.unused_vaass.append(v)
        
        return L_cp_dic, self.unused_vaass

    def CVaaS_evaluation(self, composite_vaass, path_of_regions):

        """
        Evaluate a composit VaaSs (a candidate solution) 
        A composit VaaSs has a the follwing stucture: [{'vaas':uid_vaas, 'regions':[id_region]}]        
        Args:
            composite_vaass: the composite VaaSs 
            path_of_regions: path of regions that VaaSs in composite_vaass  can traversed
            return: fintness            
        """
        cost =0
        time =0
        reputation =0
        availability =1
        # store a map of <region, distance> from the path
        region_distance ={}
        for r in path_of_regions['regions']:
            for p in path_of_regions['paths']:
                if p['uid'] == r:
                    region_distance.update({r:p['weight']})

        # calcule cost, time, availability, and reputaiton of the composition
        vaaSs_composite={} # couple <vaas, fitness>
        for vaas in composite_vaass:            
            reputation+= vaas["vaas"].get_reputation()
            availability *=vaas["vaas"].get_availability()
            cost_local =0
            time_local = 0
            for r in vaas["regions"]:
                cost+= vaas["vaas"].get_cost(region_distance.get(r))
                cost_local+=vaas["vaas"].get_cost(region_distance.get(r))

                time+= vaas["vaas"].get_time(region_distance.get(r))
                time_local+= vaas["vaas"].get_time(region_distance.get(r))
            totale_vaas = self.weights[0]*cost_local + self.weights[1]*time_local + self.weights[2]*reputation + self.weights[3]*availability
            vaas["vaas"].update_fitness(totale_vaas)
            vaaSs_composite.update({vaas["vaas"]:totale_vaas})
        
        totale = (self.weights[0]*cost + self.weights[1]*time + self.weights[2]*reputation + self.weights[3]*availability)/len(composite_vaass)

        return cost, time, reputation, availability, totale, vaaSs_composite
    

    def cVaaS_adjustment(self, composition_Vaas, fitness_composition, paths):
        """ replacing the worst VaaS representative with a fitter one
        
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        fitness_tmp = {}
        for vaas in composition_Vaas:
            f = vaas["vaas"].fitness()
            # to evaluate the worstness of a vaas we multply it's fitness by the nymber of violated QoS (place, rating)
            fitness_tmp.update({vaas["vaas"]:f*vaas["vaas"].violation(self.user_query['QoS'])}) 

        # sorted the dictionary of <vaas, vaas_fitness*number_violation>
        # the higher the vaas_fitness*number_violation is, the vaas in the more affecting the global fitness => vaas is the worest
        sorted_vaas = dict(sorted(fitness_tmp.items(), key=lambda x:x[1], reverse=True)) 
        worst_vaas = next(iter(sorted_vaas))
        # How to subsituate the worst vaaS, in this version, with a another vaas that cover the same regions covred by the worst 

        substitors = [v for v in self.unused_vaass if worst_vaas.covered_regions == v.covered_regions]                        
        if len(substitors)>0:                            
            #2. sorted the  set of cover_first_region according to the number of covred regions
            for vaas in composition_Vaas:
                if vaas["vaas"] == worst_vaas:
                    vaas["vaas"] = worst_vaas

            self.unused_vaass.append(worst_vaas)
        
        else: # it's not possible de sustituate the worst vaas 
            pass
        

    #check if a compositon is feasible 
    def check_feasible(self, composition, regions):

        # identify the set of region convered by the composition
        listtmp=[]
        for item in composition:
            listtmp+= item["regions"]
        
        ar1 = np.array(listtmp)
        ar2 = np.array(list(regions))
        # check if all regions are coverd by list
       
        return (ar1 == ar2).all()
    
   
    def contains_id(self, objects, search_id):

        """check if uiid object exist in a list of object        
        arguments:
            objects -- the list of objects 
            search_id: the id searched
        Return: True of False
        """        
        return any(obj.uid == search_id for obj in objects)
    
    def run(self):
        """The main program         
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        # 1. genere path of traversed regions

        #2. generate intiale solutions using candidate_CVaaS function
        for it in range(0, self.iterations):
            # ici on execute chaque iteration
            # generation des solution condidates; composite_vaaS
            # Evaluaiton 
            # Ajustement 
            print()
          
    
    




                

        
            


