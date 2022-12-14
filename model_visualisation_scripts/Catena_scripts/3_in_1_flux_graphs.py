#IMport the pacakges
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat
#Import the data_
#Import the data_
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/0_1mm_nonlinear/'

print('This is the input file directory: '+DataDirectory)
#Load all the data
print('Load the flowtube data')
ft_out = pd.read_csv(DataDirectory+'0mm_mixing_full_cosmo/ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
print('Load the eroded particle data')
eroded_bins = pd.read_csv(DataDirectory+'0mm_mixing_full_cosmo/ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('Load the particle data')
bins = pd.read_csv(DataDirectory+'0mm_mixing_full_cosmo/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


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

# #Fluxes
print('Creating the flux figures...')
#Plot the lower flux boxplot
fig = plt.figure(figsize =(18,6))
ax = plt.subplot(1,3,1)
plot_bins = [[] for i in (time_unique)]
for i in range(0,len(time_unique)):
    temp_bins=eroded_bins[(eroded_bins['time'] == time_unique[i]) & (eroded_bins['bn'] == eroded_bins.bn.max())]
    plot_bins[i] = np.append(plot_bins[i], [temp_bins['be_conc']])
c="k"
ax.boxplot(plot_bins,showmeans=True,showfliers=False,labels=timelabels, patch_artist=True,
            boxprops=dict(facecolor='None', color=c),
            capprops=dict(color=c),
            whiskerprops=dict(color=c),
            flierprops=dict(color=c, markeredgecolor=c),
            medianprops=dict(color=c),meanprops=dict(marker='o',markerfacecolor=c,markeredgecolor=c),)
ax.set_title('No Mixing',fontsize=12)
ax.set_xticklabels(timelabels.astype(int))


#Import the data_
print('Load the flowtube data')
ft_out = pd.read_csv(DataDirectory+'1mm_mixing_full_cosmo/ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
print('Load the eroded particle data')
eroded_bins = pd.read_csv(DataDirectory+'1mm_mixing_full_cosmo/ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('Load the particle data')
bins = pd.read_csv(DataDirectory+'1mm_mixing_full_cosmo/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


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
ax = plt.subplot(1,3,2)
plot_bins = [[] for i in (time_unique)]
for i in range(0,len(time_unique)):
    temp_bins=eroded_bins[(eroded_bins['time'] == time_unique[i]) & (eroded_bins['bn'] == eroded_bins.bn.max())]
    plot_bins[i] = np.append(plot_bins[i], [temp_bins['be_conc']])
c="black"
ax.boxplot(plot_bins,showfliers=False,showmeans=True,labels=timelabels, patch_artist=True,
            boxprops=dict(facecolor='None', color=c),
            capprops=dict(color=c),
            whiskerprops=dict(color=c),
            flierprops=dict(color=c, markeredgecolor=c),
            medianprops=dict(color=c),meanprops=dict(marker='o',markerfacecolor=c,markeredgecolor=c),)
ax.set_title('1mm Mixing',fontsize=12)
ax.set_xticklabels(timelabels.astype(int))

print('Load the flowtube data')
ft_out = pd.read_csv(DataDirectory+'10mm_mixing_full_cosmo/ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
print('Load the eroded particle data')
eroded_bins = pd.read_csv(DataDirectory+'10mm_mixing_full_cosmo/ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('Load the particle data')
bins = pd.read_csv(DataDirectory+'10mm_mixing_full_cosmo/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


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
ax = plt.subplot(1,3,3)
plot_bins = [[] for i in (time_unique)]
for i in range(0,len(time_unique)):
    temp_bins=eroded_bins[(eroded_bins['time'] == time_unique[i]) & (eroded_bins['bn'] == eroded_bins.bn.max())]
    plot_bins[i] = np.append(plot_bins[i], [temp_bins['be_conc']])
c="black"
ax.boxplot(plot_bins,showfliers=False,showmeans=True,labels=timelabels, patch_artist=True,
            boxprops=dict(facecolor='None', color=c),
            capprops=dict(color=c),
            whiskerprops=dict(color=c),
            flierprops=dict(color=c, markeredgecolor=c),
            medianprops=dict(color=c),meanprops=dict(marker='o',markerfacecolor=c,markeredgecolor=c),)
ax.set_title('10mm Mixing',fontsize=12)
ax.set_xticklabels(timelabels.astype(int))



ax =fig.add_subplot(1,1,1,frameon=False)
ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)

ax.set_ylabel('$^1$$^0$Be Concentration (atoms g$^-$$^1$)',fontsize=20)
ax.yaxis.labelpad = 14
ax.set_xlabel('Age (kiloyears)',fontsize=20)

plt.savefig(DataDirectory+'/3_in_1_fluxes.png', dpi=100, bbox_inches='tight')
