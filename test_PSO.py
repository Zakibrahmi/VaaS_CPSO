from vass import VaaS
import numpy as np
from CP_PSO_VaaS import PSO_VaaS

QoS ={'cost': 10, 'speed':20, 'availability':0.9, 'reputation': 0.8}
v1 = VaaS(10, 'bus', QoS, [0,1])
v2 = VaaS(11, 'bus', {'cost': 5, 'speed':100, 'availability':0.85, 'reputation': 0.9}, [0])
v3 = VaaS(12, 'bus', {'cost': 8, 'speed':110, 'availability':0.85, 'reputation': 0.9}, [1,3, 2, 5, 8])
vaaSSS = [v2, v1, v3]

vaaSSS = sorted(vaaSSS, key=lambda VaaS: VaaS.get_convered_regions(), reverse=True)


list_of_local_paths = {'path': 1, 'regions': {0, 1, 3}, 'paths': [{'uid': 0, 'nodes': [0, 1, 9], 'weight': 111.20748446026197}, {'uid': 1, 'nodes': [9, 28, 20], 'weight': 108.66811158549974}]}

"""
for v in L_cp:
    for i, value in enumerate(v):
        print(f"Value at index {i}: {value.uid}")
"""
L_temp =  [v for v in vaaSSS if list_of_local_paths['regions'].intersection(v.covered_regions)]

#
v = PSO_VaaS([0.25, 0.25, 0.25, 0.25])
c, unused = v.candidate_CVaaS(vaaSSS, list_of_local_paths)
cost, time, reputation, availability, total, vaas= v.CVaaS_evaluation(c[0], list_of_local_paths)
print(vaas)

