#This Script produces graphs from a succesful mixing column run

#IMport the pacakges
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/feather_runs/pomd/nonlinear_mixing_ss_new_erate/'

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

colors = plt.cm.viridis(np.linspace(0,1,len(time_unique)))


# Hillslope profile
fig = plt.figure()
ax = plt.subplot(1,1,1)
# Set up the plots based on times
for i in range(0,timesteps):
    ds_dist = ft_data[i*pits:i*pits+pits][:,0]
    elev = ft_data[i*pits:i*pits+pits][:,3]
    elev = elev-min(elev)
    cb = ax.scatter(ds_dist,elev,s=2,color=colors[i])
    cb.set_clim(vmin=0,vmax=max(time_unique))
ax.set_ylabel('Elevation (m)',fontsize=16)
ax.set_xlabel('Distance Downslope (m)',fontsize=16)
axcb = plt.colorbar(cb)
axcb.ax.set_ylabel('Time (kiloyears)',fontsize=12)

plt.tight_layout()
plt.savefig(DataDirectory+'/hillslope_profile_with_time.png', dpi=100, bbox_inches='tight')
