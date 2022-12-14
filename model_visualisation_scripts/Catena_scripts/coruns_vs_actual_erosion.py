#IMport the pacakges
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from itertools import repeat


dirname = '0_1mm_nonlinear'
folname = '0mm_mixing_full_cosmo'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/'+dirname+'/'+folname+'/'

# Load the cronus data
cronus_fname = 'cronus_data.csv'
cronus = pd.read_csv(DataDirectory+cronus_fname, sep=" ",header=None,names=['smpl', 'nuclide', 'st_d', 'st_e', 'st_int', 'st_ext' , 'lm_d', 'lm_e', 'lm_int', 'lm_ext', 'lsd_d', 'lsd_e', 'lsd_int', 'lsd_ext'] )

# load the mixing model data
mixing_fname = 'model_erosion_data'
mixing  = pd.read_csv(DataDirectory+mixing_fname, sep=" ",header=None,names=['ds_dist','elev', 'width', 'h', 'slope', 'k', 'flux','lowering' ] )

comb = pd.concat([cronus, mixing], ignore_index=True, sort=False,axis=1)
comb.columns = ['smpl', 'nuclide', 'st_d', 'st_e', 'st_int', 'st_ext' , 'lm_d', 'lm_e', 'lm_int', 'lm_ext', 'lsd_d', 'lsd_e', 'lsd_int', 'lsd_ext','ds_dist','elev', 'width', 'h', 'slope', 'k', 'flux','lowering' ]

# Sort out the time stuff
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/0_1mm_linear/0mm_mixing/'

bins = pd.read_csv(DataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )

time_unique = bins.time.unique()
time_unique = np.array(time_unique)
time_unique = time_unique/1000
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']/1000

ds_dist_unique = mixing.ds_dist.unique()
ds_dist_unique = np.array(ds_dist_unique)
# set up figure plot

colors = plt.cm.viridis(np.linspace(0,1,len(time_unique)))

fig = plt.figure(figsize =(10,5))
ax = plt.subplot(1,3,1)


# Loop through to make the graph

for j in range(0,len(ds_dist_unique)):
    temp_comb = comb[(comb['ds_dist'] == ds_dist_unique[j])]
    
    for i in range(0,len(time_unique)):
        # Find the difference between the two and express as %
        erosion = temp_comb['st_e'][i*len(ds_dist_unique)+j]/1000000/temp_comb['lowering'][i*len(ds_dist_unique)+j]
        erosion_upp = -erosion+(temp_comb['st_e'][i*len(ds_dist_unique)+j]+temp_comb['st_ext'][i*len(ds_dist_unique)+j])/1000000/temp_comb['lowering'][i*len(ds_dist_unique)+j]
        erosion_low = erosion-(temp_comb['st_e'][i*len(ds_dist_unique)+j]-temp_comb['st_ext'][i*len(ds_dist_unique)+j])/1000000/temp_comb['lowering'][i*len(ds_dist_unique)+j]
        ds_dist = temp_comb['ds_dist'][i*len(ds_dist_unique)+j]
        err = [[erosion_upp],[erosion_low]]
        
        
        # plot the % with time
        
        # cb = ax.errorbar(ds_dist,erosion,yerr=err,fmt='none',color=colors[i],s=10,zorder=1)
        cb = ax.scatter(ds_dist,erosion,color=colors[i],s=5,zorder=2)
ax.set_title('0mm mixing',fontsize=12)

folname = '1mm_mixing_full_cosmo'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/'+dirname+'/'+folname+'/'

# Load the cronus data
cronus_fname = 'cronus_data.csv'
cronus = pd.read_csv(DataDirectory+cronus_fname, sep=" ",header=None,names=['smpl', 'nuclide', 'st_d', 'st_e', 'st_int', 'st_ext' , 'lm_d', 'lm_e', 'lm_int', 'lm_ext', 'lsd_d', 'lsd_e', 'lsd_int', 'lsd_ext'] )

# load the mixing model data
mixing_fname = 'model_erosion_data'
mixing  = pd.read_csv(DataDirectory+mixing_fname, sep=" ",header=None,names=['ds_dist','elev', 'width', 'h', 'slope', 'k', 'flux','lowering' ] )

comb = pd.concat([cronus, mixing], ignore_index=True, sort=False,axis=1)
comb.columns = ['smpl', 'nuclide', 'st_d', 'st_e', 'st_int', 'st_ext' , 'lm_d', 'lm_e', 'lm_int', 'lm_ext', 'lsd_d', 'lsd_e', 'lsd_int', 'lsd_ext','ds_dist','elev', 'width', 'h', 'slope', 'k', 'flux','lowering' ]

# Sort out the time stuff
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/0_1mm_linear/0mm_mixing/'

bins = pd.read_csv(DataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )

time_unique = bins.time.unique()
time_unique = np.array(time_unique)
time_unique = time_unique/1000
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']/1000

ds_dist_unique = mixing.ds_dist.unique()
ds_dist_unique = np.array(ds_dist_unique)
# set up figure plot

colors = plt.cm.viridis(np.linspace(0,1,len(time_unique)))


ax = plt.subplot(1,3,2)


# Loop through to make the graph

for j in range(0,len(ds_dist_unique)):
    temp_comb = comb[(comb['ds_dist'] == ds_dist_unique[j])]
    
    for i in range(0,len(time_unique)):
        # Find the difference between the two and express as %
        erosion = temp_comb['st_e'][i*len(ds_dist_unique)+j]/1000000/temp_comb['lowering'][i*len(ds_dist_unique)+j]
        erosion_upp = -erosion+(temp_comb['st_e'][i*len(ds_dist_unique)+j]+temp_comb['st_ext'][i*len(ds_dist_unique)+j])/1000000/temp_comb['lowering'][i*len(ds_dist_unique)+j]
        erosion_low = erosion-(temp_comb['st_e'][i*len(ds_dist_unique)+j]-temp_comb['st_ext'][i*len(ds_dist_unique)+j])/1000000/temp_comb['lowering'][i*len(ds_dist_unique)+j]
        ds_dist = temp_comb['ds_dist'][i*len(ds_dist_unique)+j]
        err = [[erosion_upp],[erosion_low]]
        
        
        # plot the % with time
        
        # cb = ax.errorbar(ds_dist,erosion,yerr=err,fmt='none',color=colors[i],s=10,zorder=1)
        cb = ax.scatter(ds_dist,erosion,color=colors[i],s=5,zorder=2)
ax.set_title('1mm mixing',fontsize=12)


folname = '10mm_mixing_full_cosmo'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/'+dirname+'/'+folname+'/'

# Load the cronus data
cronus_fname = 'cronus_data.csv'
cronus = pd.read_csv(DataDirectory+cronus_fname, sep=" ",header=None,names=['smpl', 'nuclide', 'st_d', 'st_e', 'st_int', 'st_ext' , 'lm_d', 'lm_e', 'lm_int', 'lm_ext', 'lsd_d', 'lsd_e', 'lsd_int', 'lsd_ext'] )

# load the mixing model data
mixing_fname = 'model_erosion_data'
mixing  = pd.read_csv(DataDirectory+mixing_fname, sep=" ",header=None,names=['ds_dist','elev', 'width', 'h', 'slope', 'k', 'flux','lowering' ] )

comb = pd.concat([cronus, mixing], ignore_index=True, sort=False,axis=1)
comb.columns = ['smpl', 'nuclide', 'st_d', 'st_e', 'st_int', 'st_ext' , 'lm_d', 'lm_e', 'lm_int', 'lm_ext', 'lsd_d', 'lsd_e', 'lsd_int', 'lsd_ext','ds_dist','elev', 'width', 'h', 'slope', 'k', 'flux','lowering' ]

# Sort out the time stuff
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/0_1mm_linear/0mm_mixing/'

bins = pd.read_csv(DataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )

time_unique = bins.time.unique()
time_unique = np.array(time_unique)
time_unique = time_unique/1000
timelabels = time_unique
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']/1000

ds_dist_unique = mixing.ds_dist.unique()
ds_dist_unique = np.array(ds_dist_unique)
# set up figure plot

colors = plt.cm.viridis(np.linspace(0,1,len(time_unique)))


ax = plt.subplot(1,3,3)


# Loop through to make the graph

for j in range(0,len(ds_dist_unique)):
    temp_comb = comb[(comb['ds_dist'] == ds_dist_unique[j])]
    
    for i in range(0,len(time_unique)):
        # Find the difference between the two and express as %
        erosion = temp_comb['st_e'][i*len(ds_dist_unique)+j]/1000000/temp_comb['lowering'][i*len(ds_dist_unique)+j]
        erosion_upp = -erosion+(temp_comb['st_e'][i*len(ds_dist_unique)+j]+temp_comb['st_ext'][i*len(ds_dist_unique)+j])/1000000/temp_comb['lowering'][i*len(ds_dist_unique)+j]
        erosion_low = erosion-(temp_comb['st_e'][i*len(ds_dist_unique)+j]-temp_comb['st_ext'][i*len(ds_dist_unique)+j])/1000000/temp_comb['lowering'][i*len(ds_dist_unique)+j]
        ds_dist = temp_comb['ds_dist'][i*len(ds_dist_unique)+j]
        err = [[erosion_upp],[erosion_low]]
        
        
        # plot the % with time
        
        # cb = ax.errorbar(ds_dist,erosion,yerr=err,fmt='none',color=colors[i],s=10,zorder=1)
        cb = ax.scatter(ds_dist,erosion,color=colors[i],s=5,zorder=2)
ax.set_title('10mm mixing',fontsize=12)



cb.set_clim(vmin=0,vmax=max(time_unique))
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.1, 0.02, 0.78])
axcb = plt.colorbar(cb, cax=cbar_ax)
axcb.ax.set_ylabel('Time (kiloyears)',fontsize=12)

ax =fig.add_subplot(1,1,1,frameon=False)
ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)


ax.set_xlabel('Distance Downslope (m)',fontsize=20)


ax.set_ylabel('CRN derived erosion rate/Local erosion rate',fontsize=12)

ax.set_xlim(0,max(ds_dist_unique))

plt.savefig(DataDirectory+'erosion_compared.png', dpi=100, bbox_inches='tight')
plt.show()