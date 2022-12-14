

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
mean_crn =np.zeros((len(time_unique),len(bins_unique)//2))
print('Creating the depth profiles figures...')
#Hillslope CRN figure

for i in range(0,len(time_unique)):
    thick = ft_data[i*pits:i*pits+pits][:,5]
    # thick = [x for item in thick for x in repeat(item,2)]
    for j in range(0,len(bins_unique)//2):
        
        # temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] == bins_unique[j]) & (bins['d_loc'] <= thick[j])]
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] >= bins_unique[j*2]) & (bins['bn'] <= bins_unique[j*2+1]) & (bins['d_loc'] < thick[j])]
        mean_crn[i,j] = (temp_bins.mean().be_conc)
# print(mean_crn)        
w=0
fig = plt.figure(figsize =(15,10))
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
        
        ax = plt.subplot(2,3,w)
        for i in range(0,len(time_unique)):
            thick = ft_data[i*pits:i*pits+pits][:,5]
            # thick = [x for item in thick for x in repeat(item,2)]
            for j in range(0,len(bins_unique)//2):
                
                # temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] == bins_unique[j]) & (bins['d_loc'] <= thick[j])]
                temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] >= bins_unique[j*2]) & (bins['bn'] <= bins_unique[j*2+1]) & (bins['d_loc'] < thick[j])]
                temp_crn = temp_bins.mean().be_conc
                # print(temp_crn)
                temp_crn = (temp_crn/mean_crn[i,j])*100-100
                cb = ax.scatter((bins_unique[j*2+1]/2),temp_crn,color=colors[i],s=10)
                cb.set_clim(vmin=0,vmax=max(time_unique))
        ax.set_xlim(0,max(bins_unique)/div)
        ax.set_ylim(-15,15)
        # axcb = plt.colorbar(cb)
        ax.set_title(str(part_insert)+' particles per kg')
fig.subplots_adjust(right=0.8)
ax =fig.add_subplot(1,1,1,frameon=False)
ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)        

ax.set_ylabel('$\%$ difference with Volumetric insertion mean $^1$$^0$Be Concentration in soil_column (atoms g$^-$$^1$)',fontsize=12)
ax.set_xlabel('Distance Downslope (m)',fontsize=20)

cbar_ax = fig.add_axes([0.85, 0.1, 0.02, 0.78])
axcb = plt.colorbar(cb, cax=cbar_ax)
axcb.ax.set_ylabel('Time (kiloyears)',fontsize=12)

plt.savefig(DataFolder+'/particle_insert_sensitivity.png', dpi=100, bbox_inches='tight')


# Loop through and do the same for profiles

# for subdirs, dirs, files in os.walk(DataFolder):

#     for dirs in lst:
#         w = w+1
#         print(w)
        
#         ft_out = pd.read_csv(DataFolder+str(dirs)+'/ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
        
#         eroded_bins = pd.read_csv(DataFolder+str(dirs)+'/ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
#         # print('Load the particle data')
#         bins = pd.read_csv(DataFolder+str(dirs)+'/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )

#         # model run
#         model_run_in = pd.read_csv(DataFolder+str(dirs)+'/CRN_trans_param.CRNparam',header=None, sep=" ")
#         part_insert = model_run_in[1][4]
#         # General Profiles
        
#         # Set up the ds distances

#         ft_pits = ft_out.s.unique()
#         ft_pits = np.array(ft_pits)
#         ft_pits = np.delete(ft_pits, np.where(ft_pits == '-99'))
#         ft_pits = np.delete(ft_pits, np.where(ft_pits == 's'))
#         ft_pits = ft_pits.astype(np.float)
#         # print(ft_pits)
#         ft_data = ft_out
#         ft_data = ft_data.drop(ft_data[(ft_data.s == 's') | (ft_data.s == '-99')].index)
#         ft_data = np.array(ft_data)
#         ft_data = ft_data.astype(np.float)






#         timesteps = int(len(ft_data)/len(ft_pits))
#         pits = int(len(ft_pits))



#         time_unique = bins.time.unique()
#         time_unique = np.array(time_unique)
#         time_unique = time_unique/1000
#         timelabels = time_unique
#         bins_unique = bins.bn.unique()
#         bins_unique = np.array(bins_unique)
#         bins['time'] = bins['time']/1000
#         eroded_bins['time'] = eroded_bins['time']/1000
#         div = max(bins_unique)/max(ft_pits)

#         colors = plt.cm.viridis(np.linspace(0,1,len(time_unique)))
#         # IMport the volumetric data

#         # Loop through and make a series of graphs for average BE conc
#         # first extract the base data and save it

#         print('Creating the depth profiles figures...')
#         #Hillslope CRN figure
        
#         ax = plt.subplot(2,3,w)
#         for i in range(0,len(time_unique)):
#             thick = ft_data[i*pits:i*pits+pits][:,5]
#             # thick = [x for item in thick for x in repeat(item,2)]
#             for j in range(0,len(bins_unique)//2):
                
#                 # temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] == bins_unique[j]) & (bins['d_loc'] <= thick[j])]
#                 temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] >= bins_unique[j*2]) & (bins['bn'] <= bins_unique[j*2+1]) & (bins['d_loc'] < thick[j])]
#                 temp_crn = temp_bins.mean().be_conc
#                 # print(temp_crn)
#                 temp_crn = (temp_crn/mean_crn[i,j])*100-100
#                 cb = ax.scatter((bins_unique[j*2+1]/2),temp_crn,color=colors[i],s=10)
#                 cb.set_clim(vmin=0,vmax=max(time_unique))
#         ax.set_xlim(0,max(bins_unique)/div)
#         ax.set_ylim(-15,15)
#         axcb = plt.colorbar(cb)
#         ax.set_title(str(part_insert)+' particles per kg')
