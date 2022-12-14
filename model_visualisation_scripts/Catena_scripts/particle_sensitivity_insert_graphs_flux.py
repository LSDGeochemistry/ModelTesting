

#IMport the pacakges
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat
import os
#Import the data_
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/sensitivity_tests/analytical_linear_test_upgraded_mm/'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/steady_state_tests/analytical_linear_test_neutron/'
print('Load the flowtube data')
ft_out = pd.read_csv(DataDirectory+'ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
print('Load the eroded particle data')
eroded_bins = pd.read_csv(DataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('Load the particle data')
bins = pd.read_csv(DataDirectory+'p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )

# General Profiles
print('Creating the profile figures...')
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
mean_crn =np.zeros(len(time_unique))

#Hillslope CRN figure
labels = [0]
for i in range(0,len(time_unique)):

        temp_bins = eroded_bins[(eroded_bins['time'] == time_unique[i])]

        mean_crn[i] = (temp_bins.median().be_conc)
    
print(mean_crn)   
      
w=0
fig = plt.figure(figsize =(15,10))
ax = plt.subplot(1,1,1)
#Import the data_
DataFolder = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/sensitivity_tests/particle_inserts/'

for subdirs, dirs, files in os.walk(DataFolder):

    for dirs in sorted(dirs):
        w = w+1
        print(w)
        
        ft_out = pd.read_csv(DataFolder+str(dirs)+'/ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
        
        eroded_bins = pd.read_csv(DataFolder+str(dirs)+'/ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
        # print('Load the particle data')
        bins = pd.read_csv(DataFolder+str(dirs)+'/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )

        # model run
        model_run_in = pd.read_csv(DataFolder+str(dirs)+'/CRN_trans_param.CRNparam',header=None, sep=" ")
        part_insert = model_run_in[1][4]
        # General Profiles
        
        labels.append(str(part_insert))
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

        colors = plt.cm.viridis(np.linspace(0,1,len(time_unique)))
        # IMport the volumetric data

        # Loop through and make a series of graphs for average BE conc
        # first extract the base data and save it

        print('Creating the depth profiles figures...')
        #Hillslope CRN figure
        
        
        for i in range(0,len(time_unique)):
        

                
            temp_bins = eroded_bins[(eroded_bins['time'] == time_unique[i])]
            temp_crn = temp_bins.median().be_conc
            # print(temp_crn)
            temp_crn = (temp_crn/mean_crn[i])*100-100
            cb = ax.scatter(w,temp_crn,color=colors[i],s=10)
            
        
        ax.set_ylim(-15,15)

        
       

ax.set_ylabel('$\%$ difference with Volumetric insertion median $^1$$^0$Be Concentration in flux (atoms g$^-$$^1$)',fontsize=12)
ax.set_xticklabels(labels)
ax.set_xlabel('Particles per kg',fontsize=20)

cb.set_clim(vmin=0,vmax=max(time_unique))
axcb = plt.colorbar(cb)
axcb.ax.set_ylabel('Time (kiloyears)',fontsize=12)

plt.savefig(DataFolder+'/particle_insert_sensitivity_flux.png', dpi=100, bbox_inches='tight')


