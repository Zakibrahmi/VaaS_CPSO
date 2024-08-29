from igraph import *
import random
import numpy as np

class Region():
    
    def __init__(self, name, numberNodes,numEdges, uid_from):
        
        self.numEdges = numEdges
        self.numberNodes = numberNodes 
        self.name = name
        #Gnenrate the graph         
        g=  Graph.Erdos_Renyi(n = numberNodes, p = 0.5, directed= True, loops= False)
        #self.graph= g.simplify()  # Remove self-loops
        # set atributes to nodes
        x = uid_from
        for i in g.vs:
            i["id"] = x
            x = x+1        
        #Set up of edges 
        for e in range(len(g.es)):
            g.es[e]["weight"]= random.uniform(20, 100) #Disance between 20 and 100 km
            #g.es[e]["maxSpeed"]= random.uniform(40, 120) #Speed betwwen 40 and 120 km/h
            #g.es[e]["weight"]=  g.es[e]["distance"] 
           
        self.linkedRegions = [] # Array of dictionnary. [{"Region": "R1", "Nodes": [N1, N2, ..Nn]}, ..]
        self.graph =g
    
    def addlinkedRegion(self, region, nodes): 
        """To link current region to another region "region" according to "nodes"        
           # parms: 
                region
                uuid
                nodes: array of frontier nodes. A link is dictionnary  {"Region": "R1", "Nodes": [N1, N2, ..Nn]}        """             
        
        exist = np.isin(np.array(nodes), np.array(self.graph.vs["id"]))
        if False not in exist:
            self.linkedRegions.append({"Region":region, "Nodes":nodes})
        else:
            print("connot link")
            
    # check if the current region is contains a node n
    def containsNode(self, n):        
        return n in np.array(self.graph.vs["id"])
    
    def getName(self):
        return self.name
    
    def printVertexRegion(self):        
        for e in self.graph.vs:
            print(e)
    def printEdgeRegion(self): 
        print(self.graph.get_edgelist())
        
    def printEdgeRegionObject(self):        
        for e in self.graph.es:
            print(e)    
          
    def getLinkedregions(self):
        return self.linkedRegions

    def getFrontierNode(self, regionUid): 
        
        for r in self.linkedRegions:
            if r["Region"] == regionUid:
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
        #print(list(set(path_uid)))
       
        return {"uid_region":self.getName(), "nodes": list(set(path_uid)), "weight":distance } # name of the region, path array of id vertex
        
        
     
        
        
        
              
        
        

        
		
      
 	 