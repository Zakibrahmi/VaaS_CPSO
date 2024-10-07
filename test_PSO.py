from network_smart.vass import VaaS
import numpy as np
from composition.CP_PSO_VaaS import PSO_VaaS
from network_smart.region import Region

QoS ={'cost': 1, 'speed':150, 'availability':0.9, 'reputation': 0.9}

v1 = VaaS(10, 'bus', QoS, [0], 1, 1)
v2 = VaaS(11, 'bus', {'cost': 2, 'speed':150, 'availability':0.9, 'reputation': 0.9}, [1], 3, 9)
v3 = VaaS(12, 'bus', {'cost': 1, 'speed':200, 'availability':0.99, 'reputation': 0.9}, [0], 1, 2)
v4 = VaaS(13, 'bus', {'cost': 1, 'speed':160, 'availability':0.99, 'reputation': 0.9}, [0], 1, 2)
vaaSSS = [v1, v2, v3]
VaaS.generate_random_vaas(['0', '1', '2'],['car', 'bus'], 5)
#vaaSSS = sorted(vaaSSS, key=lambda VaaS: VaaS.get_convered_regions(), reverse=True)

list_of_local_paths = {'path': 1, 'regions': {0, 1, 3}, 'paths': [{'uid': 0, 'nodes': [0, 1, 9], 'weight': 111.20748446026197}, {'uid': 1, 'nodes': [9, 28, 20], 'weight': 108.66811158549974}]}
"""
# 1. generate path of traversed regions
r1= Region(0, 10, 15,0)
r2= Region(1, 20,30,9)
r1.addlinkedRegion(1, [9])
#print(r2.graph.vs.find(id=9).index)
regions =[]
regions.append(r1)
regions.append(r2)

QoS_query ={'source': 1,'destination':20, 'QoS':{'cost': 8, 'speed':100, 'availability':0.98, 'reputation': 0.8, 'place':2, 'rating':8}}
v = PSO_VaaS([0.25, 0.25, 0.25, 0.25],vaaSSS, QoS_query, regions )
"""
#c, unused = v.candidate_CVaaS(list_of_local_paths)
#cost, time, reputation, availability, total, vaas= v.CVaaS_evaluation(c[0], list_of_local_paths)
#print(f"avant: {c[0]}")
#v.run(5)
#print(v.best_solution.to_print())
