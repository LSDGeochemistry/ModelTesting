# -*- coding: utf-8 -*-
"""
Created on Mon May  21 16:11:54 2019

@author: LHMK
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob

###User defined parameter for plotting
#Number of profiles (bins)
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/flux_tests/mixing_0_0001/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/flux_tests/mixing_0_0001_erosion_0_001/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/flux_tests/no_mixing/'
DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/flux_tests/no_mixing_erosion_0_001/'
n_bins = 12
print('This is the input file directory: '+DataDirectory)
bins = pd.read_csv(DataDirectory+'p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('loaded the particle file')

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for i in range(n_bins):
    temp_bins=bins[bins['bn'] == i]
    ax = fig.add_subplot(4,3,i+1)
    cb = ax.scatter(temp_bins["be_conc"], temp_bins["page"],s=0.1,c=temp_bins['bn'],cmap=plt.cm.viridis, label = 'Downslope Bin', lw = 0, alpha=0.25)
    cb.set_clim(vmin=0,vmax=n_bins-1)
    
plt.savefig(DataDirectory+'hillslope_crn_conc_bins_age', dpi=100, bbox_inches='tight')

fig = plt.figure()
for i in range(n_bins):
    temp_bins=bins[bins['bn'] == i]
    ax = fig.add_subplot(4,3,i+1)
    plt.hist(temp_bins['be_conc'])
    
plt.savefig(DataDirectory+'hillslope_crn_conc_bins_hist', dpi=100, bbox_inches='tight')    
    
plot_bins = [[] for i in range(n_bins)]
print(len(plot_bins))
for i in range(n_bins):
    temp_bins=bins[bins['bn'] == i]
    plot_bins[i] = np.append(plot_bins[i], [temp_bins['be_conc']])
    
fig = plt.figure()
print(len(plot_bins))
ax = fig.add_subplot(1,1,1)   
ax.boxplot(plot_bins)
plt.savefig(DataDirectory+'hillslope_crn_conc_bins_box', dpi=100, bbox_inches='tight')

    
