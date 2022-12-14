#IMport the pacakges

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat
from matplotlib.cm import ScalarMappable


depth = np.arange(0,2.0,0.1)
density = np.full_like(depth,1325)
dloc = depth*density*0.1
gamma = [160,1459.76761923,11039.2402217,4320]
scaling = [1.6783,0.01464,0.002547,0]
lambda_s = 500*np.power(10.0,-9)
erosion = 0.004
p_0 = 4.075213
cum_tot=0
for i in range (0,4):
    tot = (np.exp(-dloc/gamma[i])*scaling[i]*gamma[i])/(erosion+gamma[i]*lambda_s)
    cum_tot = cum_tot+(tot*p_0)
full_mix_tot = cum_tot[0]
print(full_mix_tot)