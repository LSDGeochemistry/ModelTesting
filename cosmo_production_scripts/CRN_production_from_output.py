# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 16:04:44 2018

@author: LHMK
"""

import matplotlib.pyplot as plt
import numpy as np

#data2 = np.genfromtxt('C:/Workspace/github/LSDMixingModel/Runs/run4_SNBG_orig/p_trans_out.pout', delimiter=' ',skip_header=0, names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','c_conc','ne_conc'])
data2 = np.genfromtxt('C:/Workspace/github/LSDMixingModel/Runs/fallout_test/p_trans_out.pout', delimiter=' ',skip_header=0, names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'])


fbe_conc =data2['fallout_be_conc']
be_conc =data2['be_conc'] 
#Depth   
d_loc =data2['d_loc']
#distance downslope
s_loc =data2['s_loc']
#Elevation
z_loc =data2['z_loc']
#print max(be_conc)
#PLot the figure
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
#ax.plot(c_z,z, label = 'Lal and Chen Analytical Model')

plt.tick_params(axis='both', which='major', labelsize=8)
ax.scatter(fbe_conc,d_loc,c='k',s= 0.4, label = 'Mixing Model')
#cb = ax.scatter(s_loc, z_loc,c=be_conc, cmap=plt.cm.YlOrBr, s= 10, label = 'Be Concentration', lw = 0)
ax.set_xlabel("Be Conc")
ax.set_ylabel("Depth (m)")
#ax.set_xlim(0,1000)
#ax.set_ylim(112,114)
#axcb = plt.colorbar(cb)
#cb.set_clim(vmin=0,vmax=20000)
#axcb.ax.tick_params(labelsize=1)
#axcb.set_label('$^{10}$Be Concentration', size=15)
#plt.savefig('test_hillslope_crn_conc_mix_0.1.png', dpi=800, bbox_inches='tight')
#plt.savefig('test_hillslope_crn_conc_bins', dpi=800, bbox_inches='tight')
plt.gca().invert_yaxis()