
from igraph import *
import igraph as ig
from network_smart.region import *

class network_region:

    def __init__(self, filename):
        """ network is created from a text file"""
        self.file = filename

    def read_edges_vertexs_from_file(self):
        """Read edges from a text file and return as a list of edges and vertex."""
        
        edges = []
        vertexs = set()
        with open(self.file, 'r') as file:
            for line in file:
                u, v = map(int, line.strip().split())
                u= u-1
                v = v-1
                edges.append((u, v))
                vertexs.add(u)
                vertexs.add(v)
        return edges, vertexs
    
    def regions_built(self, number_regions=3):

        edges, vertex = self.read_edges_vertexs_from_file()
        # Create the graph
        g = ig.Graph(directed=False)
        v = [str(i) for i in range(0, len(vertex))]
        edges = [(str(a), str(b)) for a, b in edges]			
        g.add_vertices(v)
        g.add_edges(edges)
        g.vs['id'] = g.vs['name']
        
        # Find connected components
        components =  g.community_leading_eigenvector()
        #print(components)
        regions ={}
        for i, community in enumerate(components):
            # Create a subgraph for the community and create region
            re= Region(i, g.subgraph(community))
            regions.update({i:re})
        
        # connect graphs:  for each graph g find it connected graph g2 
        #                 regarding a a edge contains item beglongs to the 2 graph
        checked =[]
        for k, g in regions.items():
            #1. find shared edge of a candidate regions
            # Find tuples where the first item is in the array and the second item is not
            shared_tuples = [t for t in edges if t[0] in g.graph.vs["id"] and t[1] not in g.graph.vs["id"]]
            if shared_tuples:
                n = shared_tuples[0][1]
                g.graph.add_vertices(n)
                g.graph.vs[len(g.graph.vs)-1]['id'] = str(n)
                #g.graph.add_vertices(str(n))
            #2. Find the concret region g2, which has an item of shared_tuples
            for key, cg in regions.items():
                if key!= k: 
                    id_key =  set(cg.graph.vs["id"])
                    id_k = set(g.graph.vs["id"])
                    
                    intersection = id_key.intersection(id_k)
                    if intersection and (k, key) not in checked and (key, k) not in checked:
                        checked.append((k, key))
                        # add link between the 2 regions
                        g.addlinkedRegion(cg, intersection)                                              

        return regions, checked
             
