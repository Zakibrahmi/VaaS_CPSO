
from utils.util import *
from mealpy import IntegerVar, WOA, Problem


class composite_vaas(Problem):

    """ A composite Vaass, which is a solution, is a an array of dictionary: [{'uidvaas': vaas, 'regions': [array of traversed regions of the given path]}]	
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    def __init__(self, path_regions, weights,query,  set_vaas,composite_solution=None, bounds=None, minmax="min", objective_function="all", **kwargs):
        self.solution = composite_solution
        self.best_vaas =None
        self.worst_vaas = None
        self.fitnes =0
        self.path_of_regions=path_regions
        self.weights = weights
        self.vaas_set = set_vaas
        self.user_query = query
        self.objectiveF= objective_function # can be cost, availability, reputation, or all (fitness function)
        if bounds:
            super().__init__(bounds, minmax, **kwargs)
    
    def update_current_solution(self, solution):
        self.current_solution = solution
    def update_best_vaas(self, vaas):
        self.best_vaas = vaas
    def update_worst_vaas(self, vaas):
        self.worst_vaas = vaas
    def get_best_vaas(self):
        return self.best_vaas
    def get_worst_vaas(self):
        return self.worst_vaas
    def get_current_solution(self):
        return self.current_solution

    
    def obj_func(self, x=None):
        """
        Evaluate a composit VaaSs (a candidate solution) 
        A composit VaaSs has a the following stucture: [{'vaas':object_vaas, 'regions':[id_region]}]        
        return: fitness            
        """
        
        # to be able to use the function as the objetcive function of PSO and others algorithms of mealpy        
        if x is not None: # X is a solution from PSO for example, but not  CP_PSO
            x_decoded = self.decode_solution(x)
            x = x_decoded["vaas_var"]
            # Transform solution x as arry of {'vaas": object_vaas, "regions": array of uid_region}
            # x is a an array where each cell contains indice of vaas, and it's indice representes indice of region
            solutionX=[]
            tmp = x.copy()
            for it in x: 
              if it in tmp: # means that it not yet procedded
                indices = self.find_indices(it, x)
                solutionX.append({"vaas":self.find_vaas_By_Id(vaas_set=self.vaas_set, uid=it), "regions":indices})
                tmp = [item for item in tmp if item != 3]
            self.solution = solutionX
        #print(self.path_of_regions)
        
        cost =0
        time =0
        reputation =1
        availability =1
        # store a map of <region, distance> from the path
        region_distance ={}
        for r in self.path_of_regions['regions']:
            for p in self.path_of_regions['paths']:
                if str(p['uid_region']) == str(r):
                    region_distance.update({r:p['weight']})

        # Calcule cost, time, availability, and reputaiton of the composition
        vaaSs_composite={} # couple <vaas, fitness>
        penalty =0
        for vaas in self.solution:            
            reputation*= vaas["vaas"].get_reputation()
            availability *=vaas["vaas"].get_availability()
            cost_local =0
            time_local = 0
            penalty_local=0
            for r in vaas["regions"]:
                cost+= vaas["vaas"].get_cost(region_distance.get(r))
                cost_local+=vaas["vaas"].get_cost(region_distance.get(r))

                time+= vaas["vaas"].get_time(region_distance.get(r))
                time_local+= vaas["vaas"].get_time(region_distance.get(r))
            penalty_local +=vaas["vaas"].violation(self.user_query['QoS'])
            penalty += penalty_local

            # Normalization of all value using log transformation
            log_values= log_transform([cost_local, time_local, vaas["vaas"].get_reputation(), vaas["vaas"].get_availability(), penalty_local])
            totale_vaas = self.weights[0]*log_values[0] + self.weights[1]*log_values[1] + self.weights[2]* log_values[2] + self.weights[3]*log_values[3] + log_values[4]
            vaas["vaas"].update_fitness(totale_vaas)
            vaaSs_composite.update({vaas["vaas"]:totale_vaas})

        # To penalize low reputation and availability 
        reputation = reputation/len(self.vaas_set)
        reputation = 1/reputation
        
        availability = 1/availability

        log_values = log_transform([cost, time, reputation, availability, penalty])
        totale = self.weights[0]*log_values[0] + self.weights[1]*log_values[1] + self.weights[2]* log_values[2] + self.weights[3]*log_values[3] + 0.2*log_values[4]
        self.fitnes = totale
        
        if self.objectiveF == "reputation":
            return reputation
        if self.objectiveF == "cost":
            return cost
        if self.objectiveF== "availability":
            return availability
        if self.objectiveF== "time":
            return time
        return totale # cost, time, reputation, availability, totale, vaaSs_composite
    
    def compare(self, other):
        if self.fitnes < other.fitnes:
            return True
        return False
    
    def to_print(self):
        vs = []
        for v in self.solution:
            vs.append(v["vaas"].uid)
        return {"solution": vs, "fitness":self.fitnes}
    
    def find_indices(self, arr, x):
        # List comprehension to find all indices where x occurs in arr
        #indices = [i for i, value in enumerate(arr) if value == x]
        
        return np.where(arr == x)[0]
    
    def find_vaas_By_Id(self, vaas_set, uid):
        vaas=None
        for v in vaas_set:
            if str(v.uid) == str(uid):
                vaas = v
                break
        return vaas

    
    
    

    
