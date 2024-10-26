import igraph as ig

# Function to combine a set of graphs with common nodes into a new graph
def combine_graphs(graphs):
    combined_graph = ig.Graph(directed=True)
    node_mapping = {}
    
    for graph in graphs:
        for vertex in graph.vs:
            if vertex['name'] not in node_mapping:
                node_mapping[vertex['name']] = combined_graph.add_vertex(name=vertex['name'])
        
        for edge in graph.es:
            source = graph.vs[edge.source]['name']
            target = graph.vs[edge.target]['name']
            combined_graph.add_edge(node_mapping[source], node_mapping[target], **edge.attributes())
    
    return combined_graph

# Example graphs
g1 = ig.Graph(directed=True)
g1.add_vertices(['A', 'B', 'C'])
g1.add_edges([('A', 'B'), ('B', 'C')])

g2 = ig.Graph(directed=True)
g2.add_vertices(['A', 'D', 'E'])
g2.add_edges([('A', 'D'), ('D', 'E')])

g3 = ig.Graph(directed=True)
g3.add_vertices(['C', 'F', 'G'])
g3.add_edges([('C', 'F'), ('F', 'G')])

# Combine the graphs
combined_graph = combine_graphs([g1, g2, g3])

# Print the combined graph
print(combined_graph)


