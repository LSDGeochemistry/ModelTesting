#This Script produces graphs from a succesful mixing column run

#IMport the pacakges
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat
#Import the data_

DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/feather_runs/brc/linear/'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/test_catena/'


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



# Set up the plots based on times
for i in range(0,len(time_unique)):
    fig = plt.figure()
    ax = plt.subplot(1,1,1)
    t = time_unique[i]*1000

    temp_bins = bins[(bins['time'] == time_unique[i])]

    ax.scatter(temp_bins.s_loc,temp_bins.z_loc,c=temp_bins.be_conc, cmap=plt.cm.YlOrBr,s=0.05,label = 'Be Concentration', lw = 0)










    plt.tight_layout()
    plt.savefig(DataDirectory+'/whole_catena_view'+str((time_unique[i]))+'.png', dpi=100, bbox_inches='tight')

