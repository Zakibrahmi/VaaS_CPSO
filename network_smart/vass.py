
from typing import List, Union, Tuple, Dict
import numpy as np
import random
from utils.util import *


class VaaS():
    
    def __init__(self, uid, facilities, QoS, Covred_Regions, number_places=None, rating=None):
        """_summary
		Args:
			uid (string): uid of the Vaas
			facilities (Array of String): transport facilities offered by a VaaS (e.g., connectivity)
			QoS (Dictionay): Dictionary of QoS metrics such as cost per Km,  average speed, and rating: QoS = {'cost': 10, 'speed':20, 'availability':0.9. 'reputation': 0.8}.
			Covred_Regions (Array) : Array of regions covred by VaaS
        """
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
    def generate_random_normal(min_value, max_value, mean=None, std_dev=None, size=1):
        # Set default mean and std_dev if not provided
        if mean is None:
            mean = (min_value + max_value) / 2
        if std_dev is None:
            std_dev = (max_value - min_value) / 6  # Approximately covers the range

        # Generate random numbers
        random_numbers = np.random.normal(mean, std_dev, size)

        # Clip values to the specified range
        return np.clip(random_numbers[0], min_value, max_value)
    
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
        number_violation =1       
        if QoS_user['place'] > self.number_places:
          number_violation +=1
        if QoS_user['rating'] > self.rating:
          number_violation +=1
        
        return number_violation
    
    @classmethod
    def generate_random_vaas(clf, set_name_regions, set_facilities, number_vaas:int = 50):
        """This function generates random number_vaas
        
        Keyword arguments:
            number_vaas: Number of vaas to be generate
            number_region: Number of region which indicates the set of region to be covred by vaaSs
        Return: List of vaas and csv file contains the list of vaas 
        """
        vaas_set =set()
        data =[["uid", "cost", "availability", "reputation", "speed", "coverd_regions", "facility", "number_places", "rating"]]  
        for i in range(1, number_vaas+1):
            #randmly select the set of covred regions
            coverd_regions = random.sample(set_name_regions, random.randint(1, len(set_name_regions)-1))
            #QoS ={'cost': 1, 'speed':150, 'availability':0.9, 'reputation': 0.9}
            cost = clf.generate_random_normal(1, 5) # cost from 1 to 5
            speed = clf.generate_random_normal(80, 120) #
            availability = clf.generate_random_normal(0.1, 0.98) 
            reputation = clf.generate_random_normal(0.1, 0.98) 
            QoS = {"cost":cost, "speed":speed, "availability": availability, "reputation":reputation}
            facility =  random.choice(set_facilities)  
            number_places= random.choice([2,4,6])
            rating= random.choice([1, 2, 3, 4, 5]) 
            # Create vaas
            v = VaaS(i, facility, QoS, coverd_regions, number_places, rating=rating)
            vaas_set.add(v)
            data.append([i, cost, availability, reputation, speed, coverd_regions, facility, number_places, rating])

        store_cvs(f"dataset/vaas_{number_vaas}.csv", data) 
            

    

    

        
           
