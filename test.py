from igraph import Graph, plot
import random

def create_region(num_vertices, num_edges):
    """ Create a random region as a graph. """
    region = Graph()
    region.add_vertices(num_vertices)
    
    # Set names for each vertex
    region.vs["name"] = [f"{i}" for i in range(num_vertices)]
    
    # Ensure we don't add more edges than possible in a simple graph
    possible_edges = [(i, j) for i in range(num_vertices) for j in range(num_vertices) if i != j]
    random_edges = random.sample(possible_edges, min(num_edges, len(possible_edges)))
    
    region.add_edges(random_edges)
    return region

# Parameters for regions
num_regions = 5
num_vertices_per_region = 5
max_edges_per_region = 6

# Create regions
regions = [create_region(num_vertices_per_region, max_edges_per_region) for _ in range(num_regions)]

# Create the main graph
main_graph = Graph()

# Add regions as vertices in the main graph
main_graph.add_vertices(num_regions)

# Create an edge list to connect regions
for i in range(num_regions):
    for j in range(i + 1, num_regions):
        # Randomly connect regions with a probability
        if random.random() > 0.5:  # Adjust probability as needed
            main_graph.add_edge(i, j)

# Print and visualize regions
for idx, region in enumerate(regions):
    print(f"Region {idx + 1} vertices:", region.vs["name"])  # Now this will work
    print(f"Region {idx + 1} edges:", region.get_edgelist())

# Plot each region and the main graph
for idx, region in enumerate(regions):
    plot(region, layout=region.layout("fr"), vertex_label=region.vs["name"], bbox=(300, 300), margin=20, target=f"region_{idx + 1}.png")

# Plot main graph connecting the regions
plot(main_graph, layout=main_graph.layout("fr"), vertex_label=[f"Region {i+1}" for i in range(num_regions)], bbox=(400, 400), margin=20, target="main_graph.png")
