import math
from collections import defaultdict
from utils.util import addEdge, getAllPathsRegions

class local_paths():    
    
    def __init__(self, regions):
        
        # Assumption: 1. One region can contain the source node. 
        #             2. The number of nodes that represented frontiere node betwwen 2 regions is 1. 
        
        self.setOftravsedRegions= [] #To store paths af traversed regions
        self.regions = regions #Set of regions. Each region is a graph
        self.adjacencyRegions =defaultdict(list) # link between regions is an adjacency list

    def getAdjacencyList(self):    
        for g in self.regions:
            for r in g.getLinkedregions():
                addEdge(self.adjacencyRegions, int(g.getName()), int(r["Region"]))    
   
    def computeBestPath(self, source, destination):    
        #1. All best Paths of region paths as a dictionary 
        all_best_Path = [] # Array of paths
        sourceNode = source
        uid_path=1
        region = None
        frontierNode = None
        uid_region =1
        for pr in self.setOftravsedRegions:
            sum_best_path_region =0
            paths =[]
           # print("hi" +str(len(pr)))             
            temp= list(pr)   
                   
            for  i in  range(len(pr)-1):
                region = self.getRegionById(temp[i])
                frontierNode = region.getFrontierNode(temp[i+1])
                path = region.getbestPath(int(sourceNode), int(frontierNode))
                #print( path["nodes"])
                sum_best_path_region +=path["weight"]
                paths.append(path)
                sourceNode = frontierNode
            
            #Latest region   
            pathRegion ={}          
            region = self.getRegionById(temp[len(pr)-1])
            path = region.getbestPath(int(frontierNode), int(destination))
            
            paths.append(path)
            pathRegion.update({"path": uid_path, "regions": pr, "paths":paths, "value": sum_best_path_region+path["weight"]})
            uid_region +=1
            
            all_best_Path.append(pathRegion)
            # Get the best Path
            min = 999999999999999999999
            path_Best =None
            for p  in all_best_Path:
                if p['value'] < min:
                    min = p['value']
                    path_Best=p
            
        return path_Best

    def computeAllPathsRegions(self, source, destination):
             
        visited =[False]*(len(self.regions))       
        path = []
        pathstemp= []
        getAllPathsRegions(self.adjacencyRegions, int(source), int(destination), visited, path, pathstemp)
        pathsF = []
        #print(pathstemp)
        for p in pathstemp: 
            self.setOftravsedRegions.append(set(p))        
        #return pathsF

    # Find region by it uid                
    def getRegionById(self, uid):    
        for r in self.regions:
            if r.getName() == uid:
                return r
        return None #uid dones't exist 
    
    # To compute the finale set of local paths
    def run(self, source, destination):
            
        # 1. Get source and destination region
        source_region = None
        for g in self.regions:             
            if g.containsNode(source):
                    source_region = g
                    
        destination_regions = [] # More than 1 region can be a source region
        for g in self.regions:             
            if g.containsNode(destination):
                destination_regions.append(g)
                    
        # 2. Calculate all paths of regions    
        #  Creat adjacency List of regions     
        self.getAdjacencyList()
        #  Get all paths. for each pair of source, destination
        for r in destination_regions:
           self.computeAllPathsRegions(source_region.getName(), r.getName())
        # The best  
        path = self.computeBestPath(source, destination)
        return path      
        