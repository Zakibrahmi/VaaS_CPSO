from igraph import *
import random
import numpy as np
import json
from utils.util import generate_random_normal

class Region():
    
    def __init__(self, name, graph=None, numberNodes=None,numEdges=None, uid_from=None):
        
        self.numEdges = numEdges
        self.numberNodes = numberNodes 
        self.name = name
        self.graph =graph
        if graph ==None:
            #Gnenrate the graph         
            g=  Graph.Erdos_Renyi(n = numberNodes, p = 0.5, directed= True, loops= False)
            self.graph =g
            #self.graph= g.simplify()  # Remove self-loops
            # set atributes to nodes
            x = uid_from
            for i in g.vs:
                i["id"] = x
                x = x+1        
            #Set up of edges 
        for e in range(len(self.graph.es)):
                self.graph.es[e]["weight"]= random.uniform(20, 100) #Disance between 20 and 100 km
                #g.es[e]["maxSpeed"]= random.uniform(40, 120) #Speed betwwen 40 and 120 km/h
                #g.es[e]["weight"]=  g.es[e]["distance"] 
        
            
        self.linkedRegions = [] # Array of dictionnary. [{"Region": "R1", "Nodes": [N1, N2, ..Nn]}, ..]
            
    def addlinkedRegion(self, region, nodes): 
        """ To link current region to another region "region" according to "nodes"        
           # parms: 
                region
                uuid
                nodes: array of frontier nodes. A link is dictionnary  {"Region": "R1", "Nodes": [N1, N2, ..Nn]}        """             
        exist = np.isin(list(nodes), self.graph.vs["id"])       
        if exist:
            self.linkedRegions.append({"Region":region, "Nodes":nodes})
        else:
            print("connot link")
            
    # check if the current region is contains a node n
    def containsNode(self, n):    
        return n in  list(self.graph.vs["id"])
    
    def getName(self):
        return str(self.name)
    
    def printVertexRegion(self):        
        for e in self.graph.vs:
            print(e)
    def getEdgeRegion(self): 
        return self.graph.get_edgelist()
        
    def printEdgeRegionObject(self):        
        for e in self.graph.es:
            print(e)    
          
    def getLinkedregions(self):
        return self.linkedRegions

    def getFrontierNode(self, regionUid): 
        
        for r in self.linkedRegions:
            if r["Region"].getName() == str(regionUid):
                return r["Nodes"][0]
    
    def getbestPath(self, source, destination):
        
        s = self.graph.vs.find(id=int(source)).index
        d = self.graph.vs.find(id=int(destination)).index
        results = self.graph.get_shortest_paths(s, to=d, weights=self.graph.es["weight"], output="epath")
        path_uid =[] 
              
        distance = 0        
        for e in results[0]: 
                                 
            distance += self.graph.es[e]["weight"]
            source_vertex_id = self.graph.es[e].source 
            target_vertex_id = self.graph.es[e].target            
            path_uid.append(self.graph.vs[source_vertex_id]["id"])
            path_uid.append(self.graph.vs[target_vertex_id]["id"])
       
        return {"uid_region":self.getName(), "nodes": list(set(path_uid)), "weight":distance } # name of the region, path array of id vertex
   
    @classmethod
    def create_regions(cls, number_region, min_edges, min_nodes, max_edges, max_nodes ):
        """This function generates a set of regions 
        
        Keyword arguments:
            numer_region: number of region to be created
            min_edges/min_nodes: the minimum number of edges/nodes that compose the graph of each region
        Return: set of connected regions. For simplicity, one node are shared between 2 regions
        """
        regions =[]
        uid_from=0
        for i in range(number_region):
            num_nodes = generate_random_normal(min_nodes, max_nodes)
            num_edges = generate_random_normal(min_edges, max_edges)
            r= Region(name=str(i), numberNodes=int(num_nodes),numEdges=int(num_edges), uid_from=uid_from)
            uid_from = int(num_nodes)-1 # to easly connecting region
            
            regions.append(r)
        # Create link between regions
        for i in range(number_region):
            for j in range(i + 1, number_region):
                intersection = [value for value in regions[i].graph.vs["id"] if value in regions[j].graph.vs["id"]]
                regions[i].addlinkedRegion(regions[j], intersection)

        return regions
    
    def save_to_json(self):
        """
        Function, which convert an object region to a json file
        """        
        graph_dict = {
            "nodes": [
                    {"id": v.index, "label": v["id"]} for v in self.graph.vs 
                ],
            "edges": [
                   {"source": e.source, "target": e.target, "weight": e["weight"]} for e in self.graph.es
                ]
           }
        region_json ={
            "numEdges": self.numEdges,
            "numberNodes" : self.numberNodes, 
            "name" : self.name,
            "linked_regions": self.linkedRegions,
            "graph":graph_dict
        }
        # File to store region  as a json file
        filename = f"dataset/region_{self.name}.json"

        # Save the dictionary to a JSON file
        with open(filename, 'w') as json_file:
            json.dump(region_json, json_file, indent=4)

     
        
        
        
              
        
        

        
		
      
 	 