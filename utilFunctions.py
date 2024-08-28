from igraph import *
import random
import numpy as np
from collections import defaultdict
#from local_paths import *
from generateRegion import *
import math

def genEdge(nodes, numberEdge, seed=None, p=0.5):
    
    """ 
       Choses each of the possible [n(n-1)]/2 edges with probability p. 
       This is the same as binomial_graph and erdos_renyi_graph. 
       Sometimes called Erdős-Rényi graph, or binomial graph.
       :Parameters:
       		- 'nodes': the set of nodes
        	- 'p': probability for edge creation
         	- 'seed': seed for random number generator (default=None) 
            
    
    if not seed is None: 
        random.seed(seed)     
        for u in xrange(n): 
          for v in xrange(u+1,n): 
              if random.random() < p: 
                   G.add_edge(u,v)
	"""
    edges = set()
    nodeList = range(len(nodes))
    random.seed(seed)
    while len(edges) < numberEdge:
        p1 = random.choice(nodeList)
        p2 = random.choice(nodeList)
        if p1!=p2:
        
            pair = "\"%s\",\"%s\",-" % (str(nodes[p1]["id"]), str((nodes[p2]["id"])))
            edges.add(pair)

    return  edges

#All path from source
visitedList = [[]]

def depthFirst(graph, currentVertex, visited):
    visited.append(currentVertex)
    for vertex in graph[currentVertex]:
        if vertex not in visited:
            depthFirst(graph, vertex, visited.copy())
    visitedList.append(visited)

#All paths form  source to destination
listPaths =[]
def getAllPathsRegions(graph, u, d, visited, path, pathsSet):
 
        # Mark the current node as visited and store in path
        visited[u]= True
        path.append(u)
 
        # If current vertex is same as destination, then print
        # current path[]
        current_path = path.copy()
        current_path.append(u)
        
        if u == d:
            pathsSet.append(current_path)
        
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in graph[u]:
                if visited[i]== False:                    
                    getAllPathsRegions(graph, i, d, visited, path,pathsSet )
                     
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u]= False
#Visialize Graph

def visualizeGraph(graphobject, outputname, ):
    visual_style = {}

    out_name = outputname+".png"

    # Set bbox and margin
    visual_style["bbox"] = (400,400)
    visual_style["margin"] = 27

    # Set vertex colours
   # graphobject.vs["color"] = ["red", "green", "blue", "yellow", "orange"]

    # Set vertex size
    visual_style["vertex_size"] = 45

    # Set vertex lable size
    visual_style["vertex_label_size"] = 22
    # Don't curve the edges
    visual_style["edge_curved"] = False

    # Set the layout
    my_layout = graphobject.layout_lgl()
    visual_style["layout"] = my_layout

    # Plot the graph
    #plot(graphobject, out_name, **visual_style)
    
def addEdge(gr, u, v):
        gr[u].append(v)
        
# Generate a random vector betwwen 2 points    
def generateRandomVector(point1, point2):
          
    vec = np.abs(point1 + random.uniform(0, 1) * (point1 -point2))
    return (np.ceil(vec)).astype(int)

#r1= Region(1, 4,3,0)
#for i in r1.graph.vs:
 #   print(i)