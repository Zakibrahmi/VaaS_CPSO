from igraph import *
import random
import numpy as np
from collections import defaultdict
from local_paths import *
from generateRegion import *
from mealpy import *
import numpy as np
from mealpy import IntegerVar, PSO, Problem
from utilFunctions import *
"""sumary_line

Keyword arguments:
argument -- description
Return: return_description

"""
r1= Region(0, 10, 15,0)
r2= Region(1, 20,30,9)
r1.addlinkedRegion(1, [9])
#print(r2.graph.vs.find(id=9).index)

regions =[]
regions.append(r1)
regions.append(r2)
#print(r1.getLinkedregions())
c = local_paths(regions)
res = c.run(1,20)
print(res)


