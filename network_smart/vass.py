
from typing import List, Union, Tuple, Dict
import numpy as np
import random
from utils.util import *
import ast
import os

class VaaS():
    
    def __init__(self, data=None, uid=None, facilities=None, QoS=None, Covred_Regions=None, number_places=None, rating=None):
        """ summary
        Args:
            uid (string): uid of the Vaas
            facilities (Array of String): transport facilities offered by a VaaS (e.g., connectivity)
            QoS (Dictionay): Dictionary of QoS metrics such as cost per Km,  average speed, and rating: QoS = {'cost': 10, 'speed':20, 'availability':0.9. 'reputation': 0.8}.
            Covred_Regions (Array) : Array of regions covred by VaaS
            data: contains vaas attribute values. If data not None, we create vaas from data, which is pandas Serie
        """
        if data is not None:
            self.QoS = {'cost': data["cost"], 'speed':data["speed"], 'availability':data["availability"], 'reputation': data["reputation"]}
            self.uid=data["uid"]
            self.facilities=["facility"]
            self.covered_regions =ast.literal_eval(data["coverd_regions"])
            self.number_places= data["number_places"]
            self.rating= data["rating"]
        
        else:
            self.uid = uid
            self.facilities= facilities
            self.QoS = QoS
            self.covered_regions = Covred_Regions
            self.number_places = number_places
            self.rating= rating
        self.fitness = 0
    
    # To make vaas instance comparable        
    def __eq__(self, other):       
        return self.uid == other.uid
    
    def __hash__(self):
        return hash((self.uid,))
    
    def __str__(self):
        return str(self.uid)
    
    def update_fitness(self, new_fitness):
        self.fitness= new_fitness
    def get_convered_regions(self):
        return len(self.covered_regions)
    
    def covred_regions(self):
        return set(map(int, self.covered_regions))
    
    def  get_cost(self, region_distance=None): 

        if region_distance is None:
            return self.QoS.get("cost")
        else:
            return self.QoS.get("cost")*region_distance

    def  get_time(self, region_distance=None):  

        if region_distance is None:
            return self.QoS.get("speed")
        else:
            return region_distance/self.QoS.get("speed")
    
    def get_availability(self):
        return self.QoS.get("availability")
    
    def get_reputation(self):
        return self.QoS.get("reputation")
    def get_speed(self):
        return self.QoS.get("speed")
    
    def violation(self, QoS_user):
       
        """ Worst means: 
               1. vaas features' quality is less than a user's given threshold (e.g., number of places, rating)
               2. vaas affect the whole trip constraints. It is the item that boost the trip to violate user requirements
                  In this case vaas is the item of composition that has the higher value compare to other VaaSs
         Keyword arguments:
            QoS_user: User requierments {"cost", "availability", "time", "reputation", "rating", "places"}
            fintenss_composition: fintness value the compositon: cost, time, reputation, availability, and totale
            composition_vaass: the composition
         Return: True or False
        """
        penalty = 0      
        if QoS_user['place'] > self.number_places:
            penalty += abs(QoS_user['place'] - self.number_places) * 5
        if QoS_user['rating'] > self.rating:
            penalty += abs(QoS_user['rating'] - self.rating) * 5
        if QoS_user['availability'] > self.get_availability():
            penalty += abs(QoS_user['availability'] - self.get_availability()) * 5
        if QoS_user['speed'] > self.get_speed():
            penalty += abs(QoS_user['speed'] - self.get_speed()) * 5
        if QoS_user['cost'] > self.get_cost():
            penalty += abs(QoS_user['cost'] - self.get_cost()) * 5
        if QoS_user['reputation'] > self.get_reputation():
            penalty += abs(QoS_user['reputation'] - self.get_reputation()) * 5

        return penalty
    
    def generate_subsets(self, set_name_regions, n):
        """This function generates random subset form set_name_regions, 
            ensuring that each region is selected at least once         
        Keyword arguments:
        argument -- description
        Return: return_description
        """
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
    
    @classmethod
    def generate_random_vaas(clf, set_name_regions, set_facilities, path_to_store, number_vaas:int = 50):
        """This function generates random number_vaas        
        Keyword arguments:
            number_vaas: Number of vaas to be generate
            set_name_regions: Indicates the set of region to be covred by vaaSs
            set_facilities: set of faclilities 
        Return: List of vaas and csv file contains the list of vaas 
        """
        vaas_set =set()
        selected_regions = set()  # To keep track of selected regions across all iterations
        subsets = []  # List to hold the n subsets
        data =[["uid", "cost", "availability", "reputation", "speed", "coverd_regions", "facility", "number_places", "rating"]]  
        for i in range(0, number_vaas):
            # Randmly select the set of covred regions: You ensure that each region at least is selected once
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
            coverd_regions = list(subset.copy())

            #coverd_regions = random.sample(set_name_regions, random.randint(1, len(set_name_regions)-1))
            cost = generate_random_normal(1, 5) # cost from 1 to 5
            speed = generate_random_normal(80, 120) #
            availability = generate_random_normal(0.1, 0.98) 
            reputation = generate_random_normal(0.1, 0.98) 
            QoS = {"cost":cost, "speed":speed, "availability": availability, "reputation":reputation}
            facility =  random.choice(set_facilities)  
            number_places= random.choice([2,4,6])
            rating= random.choice([1, 2, 3, 4, 5]) 
            # Create vaas data=None, uid=None, facilities=None, QoS=None, Covred_Regions=None, number_places=None, rating=None
            v = VaaS(uid=i, facilities=facility, QoS=QoS, Covred_Regions=coverd_regions, number_places=number_places, rating=rating)
            vaas_set.add(v)
            data.append([i, cost, availability, reputation, speed, coverd_regions, facility, number_places, rating])

        store_cvs(f"{path_to_store}vaas_{number_vaas}.csv", data) 
        return vaas_set
    
    @classmethod
    def create_vaas_datasets(clf, number_vaas_per_dataset, path_to_store, set_name_regions, set_facilities ):
        """ This function implements the generation of datasets of vaas.
            Each dataset is stored on a sperated csv file.        
        Aarguments:
            number_vaas_per_dataset: array of integer. Each integer indicated the number of vaas to be generate
            path_to_store: path to store files

        Return: set of csv files.
        """
        for num_vaas in number_vaas_per_dataset:   
            csv_file = f"{path_to_store}vaas_{num_vaas}.csv"
            if not os.path.exists(csv_file):      
                clf.generate_random_vaas(set_name_regions, set_facilities, path_to_store, num_vaas)
            else:
                print(f"vaas_{num_vaas}.csv exist!")


            

    

    

        
           
