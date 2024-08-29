

class composite_vaas():

    """ A composite Vaass, which is a solution, is a an array of dictionary: [{'uidvaas': vaas, 'regions': [array of traversed regions of the given path]}]	
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    def __init__(self, composite_solution):
        self.solution = composite_solution
        self.best_vaas =None
        self.worst_vaas = None
        self.fitnes =0
    
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
    
    def CVaaS_evaluation(self, path_of_regions, weights, set_vaaSs):

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
                if p['uid_region'] == r:
                    region_distance.update({r:p['weight']})

        # calcule cost, time, availability, and reputaiton of the composition
        vaaSs_composite={} # couple <vaas, fitness>
        for vaas in self.solution:            
            reputation+= vaas["vaas"].get_reputation()
            availability *=vaas["vaas"].get_availability()
            cost_local =0
            time_local = 0
            for r in vaas["regions"]:
                cost+= vaas["vaas"].get_cost(region_distance.get(r))
                cost_local+=vaas["vaas"].get_cost(region_distance.get(r))

                time+= vaas["vaas"].get_time(region_distance.get(r))
                time_local+= vaas["vaas"].get_time(region_distance.get(r))
            totale_vaas = weights[0]*cost_local + weights[1]*time_local + weights[2]*reputation + weights[3]*availability
            vaas["vaas"].update_fitness(totale_vaas)
            vaaSs_composite.update({vaas["vaas"]:totale_vaas})
        
        totale = (weights[0]*cost + weights[1]*time + (weights[2]*reputation)/len(set_vaaSs) + weights[3]*availability)/len(self.solution)
        self.fitnes = totale
        return cost, time, (reputation/len(set_vaaSs)), availability, totale, vaaSs_composite
    
    def compare(self, other):
        if self.fitnes < other.fitnes:
            return True
        return False
    
    def to_print(self):
        vs = []
        for v in self.solution:
            vs.append(v["vaas"].uid)
        return {"solution": vs, "fitness":self.fitnes}
    
    
    

    
