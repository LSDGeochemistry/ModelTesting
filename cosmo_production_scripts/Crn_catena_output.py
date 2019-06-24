# -*- coding: utf-8 -*-
"""
Created on Mon May  6 16:11:54 2019

@author: LHMK
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob

###User defined parameter for plotting
#Number of profiles (bins)

#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/no_mixing/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/hillslope_flux_test/no_mixing_erosion_0_00001/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001/'
DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001_erosion_0_001/'

n_bins = 10
print('This is the input file directory: '+DataDirectory)
bins = pd.read_csv(DataDirectory+'p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('loaded the particle file')

fig = plt.figure()
#temp_bins=bins[bins['bn'] == 0]
#print(temp_bins['time'][3])
max_conc = (bins['be_conc']).max()
print('The max Be concentration is: ')
print(max_conc)
for i in range(n_bins):
    temp_bins=bins[bins['bn'] == i]
    ax = fig.add_subplot(4,3,i+1)
    cb = ax.scatter(temp_bins["s_loc"], temp_bins["z_loc"],c=temp_bins["be_conc"], cmap=plt.cm.YlOrBr, s= 10, label = 'Be Concentration', lw = 0)
    axcb = plt.colorbar(cb)
    cb.set_clim(vmin=0,vmax=max_conc)
    #plt.gca().invert_yaxis()
plt.savefig(DataDirectory+'hillslope_crn_conc_bins', dpi=100, bbox_inches='tight')

fig = plt.figure()
for i in range(n_bins):
    temp_bins=bins[bins['bn'] == i]
    ax = fig.add_subplot(4,3,i+1)
    ax.scatter(temp_bins["be_conc"], temp_bins["d_loc"],s=0.0001,c='k') 
    ax.set_xlim(0,max_conc)
    ax.set_ylim(0,1)
    plt.gca().invert_yaxis()
plt.savefig(DataDirectory+'hillslope_crn_conc_bins_depth_profile', dpi=100, bbox_inches='tight') 

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

for i in range(n_bins):
    temp_bins=bins[bins['bn'] == i]
    cb = ax.scatter(temp_bins["be_conc"], temp_bins["d_loc"],s=0.1,c=temp_bins['bn'],cmap=plt.cm.viridis, label = 'Downslope Bin', lw = 0, alpha=0.25)
    cb.set_clim(vmin=0,vmax=n_bins-1)
ax.set_xlim(0,max_conc)
ax.set_ylim(0,1.0)    
plt.gca().invert_yaxis()    
axcb = plt.colorbar(cb)
plt.savefig(DataDirectory+'hillslope_crn_conc_bins_depth_profile_together', dpi=100, bbox_inches='tight')
#Plot a figure on top of each other

    
