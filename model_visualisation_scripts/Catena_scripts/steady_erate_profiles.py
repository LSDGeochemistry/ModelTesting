import numpy as np
import matplotlib
import matplotlib.pyplot as plt


depth = np.arange(0,200,1)
density = np.full_like(depth,1.325)
dloc = depth*density
gamma = [160,1459.76761923,11039.2402217,4320]
scaling = [1.6257852,0.014495419,0.0025436458,0]
lambda_s = 500*np.power(10.0,-9)
erosion = 0.0022
p_0 = 4.075213
cum_tot=0
for i in range (0,4):
    tot = (np.exp(-dloc/gamma[i])*scaling[i]*gamma[i])/(erosion+gamma[i]*lambda_s)
    cum_tot = cum_tot+(tot*p_0)
    print(cum_tot[0])

