import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat

DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/0_1mm_linear/0mm_mixing/'

print('This is the input file directory: '+DataDirectory)
#Load all the data
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



depth_bins =[[0,0.1],[0.1,0.2],[0.2,0.3],[0.3,0.4],[0.4,0.5],[0.5,0.6],[0.6,0.7],[0.7,0.8],[0.8,0.9],[0.9,1.0]]
ft_pits =[29.75,29.25,28.75,28.25,27.75,27.25,26.75,26.25]

# Set up the plots based on times

fig = plt.figure(figsize =(18,6))
t = time_unique[1]*1000
    # print(t)
    # Set up the different pits and plot
for j in range(0,len(ft_pits)):
    upp = ft_pits[j]+0.25
    low = ft_pits[j]-0.25
    temp_bins = bins[(bins['time'] == time_unique[1]) & (bins['s_loc'] <= upp) & (bins['s_loc'] >= low)]
        # Set up the plot
    ax = plt.subplot(1,len(ft_pits),j+1)
    ax.scatter(temp_bins.be_conc,temp_bins.d_loc,c='0.6',s=0.05)

        # print(c_z)
        # ax.plot(c_z,z/100,c='k', label = 'Lal and Chen (2005)')
        # Now do the depth n_bins
    for k in range(0,len(depth_bins)-1):
        temp = temp_bins[(temp_bins.d_loc >= depth_bins[k][0]) & (temp_bins.d_loc <= depth_bins[k][1])]
            #Find the mean values of each bi
        mean_d = temp.mean().d_loc

        mean_be = temp.mean().be_conc
        be_std = temp.std().be_conc
        d_std = temp.std().d_loc
            
        ax.errorbar(mean_be,mean_d,xerr=be_std,fmt='none',c='k',ls='--')
        ax.scatter(mean_be,mean_d,s=20,c='k')





        ax.set_ylim(0,1.0)
            
        plt.gca().invert_yaxis()
        ax.set_title('Pit '+str(j+1)+' ('+str(ft_pits[j])+'m downslope)',fontsize=12)
        if j > 0:
            ax.set_yticklabels([])

    
    

ax =fig.add_subplot(1,1,1,frameon=False)
ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
ax.set_ylabel('Depth (m)',fontsize=18)
    
ax.set_xlabel('$^1$$^0$Be Concentration atoms g$^-$$^1$',fontsize=18)


plt.tight_layout()
plt.show()