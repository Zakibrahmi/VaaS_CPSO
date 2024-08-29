
from typing import List, Union, Tuple, Dict

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
           
