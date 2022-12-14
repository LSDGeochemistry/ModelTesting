

#IMport the pacakges
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat
import os
#Import the data_
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/        

fig = plt.figure(figsize =(15,10))
ax = plt.subplot(1,1,1)
#Import the data_
DataFolder = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/sensitivity_tests/insert_depth/'
w=0
for subdirs, dirs, files in os.walk(DataFolder):
    print(len(dirs))
    colors = plt.cm.viridis(np.linspace(0,1,len(dirs)))
    for dirs in sorted(dirs):
 
        
        ft_out = pd.read_csv(DataFolder+str(dirs)+'/ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
        
        eroded_bins = pd.read_csv(DataFolder+str(dirs)+'/ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
        # print('Load the particle data')
        bins = pd.read_csv(DataFolder+str(dirs)+'/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )

        # model run
        model_run_in = pd.read_csv(DataFolder+str(dirs)+'/CRN_trans_param.CRNparam',header=None, sep=" ")
        insert_depth = model_run_in[1][0]
        # General Profiles
        
        # Set up the ds distances

        ft_pits = ft_out.s.unique()
        ft_pits = np.array(ft_pits)
        ft_pits = np.delete(ft_pits, np.where(ft_pits == '-99'))
        ft_pits = np.delete(ft_pits, np.where(ft_pits == 's'))
        ft_pits = ft_pits.astype(np.float)
        # print(ft_pits)
        ft_data = ft_out
        ft_data = ft_data.drop(ft_data[(ft_data.s == 's') | (ft_data.s == '-99')].index)
        ft_data = np.array(ft_data)
        ft_data = ft_data.astype(np.float)






        timesteps = int(len(ft_data)/len(ft_pits))
        pits = int(len(ft_pits))



        time_unique = bins.time.unique()
        time_unique = np.array(time_unique)
        time_unique = time_unique/1000
        timelabels = time_unique
        bins_unique = bins.bn.unique()
        bins_unique = np.array(bins_unique)
        bins['time'] = bins['time']/1000
        eroded_bins['time'] = eroded_bins['time']/1000
        div = max(bins_unique)/max(ft_pits)


        # IMport the volumetric data

        # Loop through and make a series of graphs for average BE conc
        # first extract the base data and save it

        
        #Hillslope CRN figure
        

        for i in range(0,len(time_unique)):
            thick = ft_data[i*pits:i*pits+pits][:,5]
            cb = ax.scatter(bins.be_conc,bins.d_loc,color=colors[w],s=1,label=str(insert_depth))
            cb.set_clim(vmin=0,vmax=len(dirs))
        ax.set_ylim(0,max(thick))
        ax.set_xlim(0,30000)
        w=w+1


            


ax.invert_yaxis()

ax.set_xlabel('Mean $^1$$^0$Be Concentration in soil column (atoms g$^-$$^1$)',fontsize=12)
ax.set_ylabel('Depth (m)',fontsize=20)


# axcb = plt.colorbar(cb)
# axcb.ax.set_ylabel('Insert Depth (m)',fontsize=12)

ax.legend(loc='upper left',title='Insert Depth (m)',fontsize=12,markerscale=12)

plt.savefig(DataFolder+'/insert_depth_sensitivity.png', dpi=100, bbox_inches='tight')


