from igraph import *
import random
import numpy as np
from collections import defaultdict
#from local_paths import *
#from network_smart.region import *
import math
import csv

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

def store_cvs(file, data):
    with open(file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        

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
        # If current vertex is same as destination
        
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

def addEdge(gr, u, v):
        gr[u].append(v)
        
# Generate a random vector betwwen 2 points    
def generateRandomVector(point1, point2):
          
    vec = np.abs(point1 + random.uniform(0, 1) * (point1 -point2))
    return (np.ceil(vec)).astype(int)

def log_transform(values, desired_sum=None):
    log_values = [np.log1p(value) for value in values]  # np.log1p is used to handle log(0) case
    if desired_sum is not None:
        log_sum = sum(log_values)
        adjusted_values = [value / log_sum * desired_sum for value in log_values]
    else:
        adjusted_values = log_values
    return adjusted_values