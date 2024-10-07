from igraph import *
import igraph as ig
import random
import numpy as np
from collections import defaultdict
from network_smart.local_paths import *
from network_smart.region import *
from mealpy import *
import numpy as np
from mealpy import IntegerVar, PSO, Problem
from utils.util import *
from network_smart.network_region import *

#from igraph import Graph
import random

from igraph import Graph

def read_edges_from_file(filename):
    """Read edges from a text file and return as a list of tuples."""
    edges = []
    with open(filename, 'r') as file:
        for line in file:
            u, v = map(int, line.strip().split())
            edges.append((u, v))
    return edges

def create_graph_from_edges(edges):
    """Create a graph from a list of edges."""
    G = Graph(edges)
    return G


def main(filename, num_subgraphs):
    edges = read_edges_from_file(filename)
    G = create_graph_from_edges(edges)
    
    # Print connected subgraphs
    """
    for i, sg in enumerate(subgraphs):
        print(f"Region {i+1}:")
        print("Nodes:", sg.vs.indices)
        print("Edges:", [(e.source, e.target) for e in sg.es])
        print()
    """
def ensure_connectivity(components, num_regions):
    """ Adjust the number of connected components to match the desired number of regions. """
    while len(components) > num_regions:
        # Merge the smallest components
        components.sort(key=len)  # Sort by size
        smallest = components.pop(0)
        next_smallest = components.pop(0)
        
        # Merge smallest and next smallest
        merged = list(set(smallest) | set(next_smallest))
        components.append(merged)
    
    return components
if __name__ == "__main__":
    filename = 'road-chesapeake.txt'  # Name of the input file
    #num_subgraphs = 10 # Number of linked regions
    #main(filename, num_subgraphs)
    nr = network_region(filename)
    regions, connection =nr.regions_built(3)
    print(connection)

    for k, g in regions.items():
        print(f"{g.name} : {g.getLinkedregions()}") 
        print('++++++++++++++++++++++++')
    """
    # Initialize an empty graph
    g = ig.Graph(directed=False)

    # Read the edges from the file
    edges = []
    vertex_ids = set()

    with open(filename, 'r') as f:
        for line in f:
            x, y = map(int, line.strip().split())
            edges.append((x, y))
            vertex_ids.add(x)
            vertex_ids.add(y)

    # Initialize the graph with the correct number of vertices
    g.add_vertices(len(vertex_ids)+1)

    # Add the edges to the graph
    g.add_edges(edges)
    
    # Create a dictionary to store node IDs
    node_ids = {vertex_id: vertex_id for vertex_id in vertex_ids}

    # Map each vertex ID to its corresponding index in the graph
    vertex_index_map = {vertex_id: idx for idx, vertex_id in enumerate(sorted(vertex_ids))}

    # Assign the "id" attribute to each vertex
    g.vs['id'] = [node_ids[vertex_id] for vertex_id in sorted(vertex_ids)]

    # Find connected components
    components = g.components()

    # Each component is a list of vertex indices
    connected_components = [g.vs[component].indices for component in components]

    # Extract and print each connected region
    for idx, component in enumerate(connected_components):
        print(f"Region {idx+1}:")
        region_nodes = g.vs[component]['id']
        region_edges = [(e.source, e.target) for e in g.subgraph(component).es]
        
        print(f"  Nodes: {region_nodes}")
        print(f"  Edges: {region_edges}")
        print()
    


    # Define edges for the road network
    edges = [ (1, 2), (2, 3), (3, 4), (4, 5), (1, 5), (5, 7), 
         (6, 7), (7, 8), (8, 6), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13)]
    edges = [(str(a), str(b)) for a, b in edges]
    
    # Create the graph
    g = ig.Graph(directed=False)
    v = [str(i) for i in range(1, 14)]
        
    g.add_vertices(v)
    g.add_edges(edges)
    #g.vs["id"] = v
    #print(len(g.vs))
    g.vs['id'] = g.vs['name']
    # Print the graph summary
    # Add vertex names for better readability (optional)
   
    # Find connected components
    components =  g.community_leading_eigenvector()
    regions ={}
    for i, community in enumerate(components):
        # Create a subgraph for the community
        regions.update({i:g.subgraph(community)})
        
        # Print the vertices and edges of the subgraph
        
        print(f"Community {i + 1}:")
        print("Vertices:", subgraph.vs['name'])
        print()
        for edge in subgraph.es:
            source_name = subgraph.vs[edge.source]['name']
            target_name = subgraph.vs[edge.target]['name']
            print(f"Edge: {source_name} - {target_name}")
        
    # connect graphs:  for each graph g find it connected graph g2 
    #                 regarding a a edge contains item beglongs to the 2 graph
    checked =[]
    print(regions.items())
    for k, g in regions.items():
        #1. find shared edge of a candidate regions
        # Find tuples where the first item is in the array and the second item is not
        shared_tuples = [t for t in edges if t[0] in g.vs["id"] and t[1] not in g.vs["id"]]
        if shared_tuples:
            n = shared_tuples[0][1]
            g.add_vertices(n)
            g.vs[len(g.vs)-1]['id'] = str(n)
        #g.add_vertices(str(shared_tuples[0][1]))
        #2. Find the concret region g2, which has an item of shared_tuples
        for key, cg in regions.items():
            if key!= k: 
                id_key =  set(cg.vs["id"])
                id_k = set(g.vs["id"])
                
                if id_key.intersection(id_k) and (k, key) not in checked and (key, k) not in checked:
                    checked.append((k, key))
                    # add link between the 2 regions    
    
    # Read the edges from the file
    edges = []
    vertex_ids = set()

    with open(filename, 'r') as f:
        for line in f:
            x, y = map(int, line.strip().split())
            x= x-1
            y = y-1
            edges.append((x, y))
            vertex_ids.add(x)
            vertex_ids.add(y)
    print(vertex_ids)
    """
    

