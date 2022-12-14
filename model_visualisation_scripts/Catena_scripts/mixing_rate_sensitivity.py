

#IMport the pacakges
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat
import os
#Import the data_
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/sensitivity_tests/analytical_linear_test_upgraded_mm/'
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/steady_state_tests/analytical_linear_test_neutron/'

fig = plt.figure(figsize =(15,10))
#Import the data_
DataFolder = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/sensitivity_tests/mixing_rates/'
w=0
for subdirs, dirs, files in os.walk(DataFolder):

    for dirs in sorted(dirs):
        w = w+1
        print(w)
        
        
        # print('Load the particle data')
        bins = pd.read_csv(DataFolder+str(dirs)+'/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )

        # model run
        model_run_in = pd.read_csv(DataFolder+str(dirs)+'/CRN_trans_param.CRNparam',header=None, sep=" ")
        part_insert = model_run_in[1][1]
        # General Profiles
        
        # Set up the ds distances








        
        # IMport the volumetric data

        # Loop through and make a series of graphs for average BE conc
        # first extract the base data and save it

        print('Creating the depth profiles figures...')
        #Hillslope CRN figure
        
        ax = plt.subplot(2,3,w)

        ax.scatter(bins.be_conc,bins.d_loc,c='0.6',s=0.05)
        ax.set_ylim(0,1)
        plt.gca().invert_yaxis()
        # axcb = plt.colorbar(cb)
        ax.set_title(str(part_insert)+' Mixing Rate (m yr$^-$$^1$)')
        ax.set_xlim(10000,20000)
        if w == 1:
            ax.set_xlim(10000,25000)
fig.subplots_adjust(right=0.8)
ax =fig.add_subplot(1,1,1,frameon=False)
ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)        

ax.set_ylabel('Soil Depth (m)',fontsize=12)
ax.set_xlabel('$^1$$^0$Be Concentration in soil column (atoms g$^-$$^1$',fontsize=20)

plt.savefig(DataFolder+'/mixing_rate_sensitivity.png', dpi=100, bbox_inches='tight')


