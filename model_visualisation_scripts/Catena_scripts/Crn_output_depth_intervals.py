#Script for plotting and comparing down  ahillsope transect
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob

###User defined parameter for plotting
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/no_mixing/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/hillslope_flux_test/no_mixing_erosion_0_00001/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001/'
# DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001_erosion_0_001/'
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/catenas_no_mixing/steep/'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/idealised_catena_runs/heavy_mixing/'
#Number of profiles (bins), should rip this straight from model output for simplicity!!!
# Do the flat section
print('This is the input file directory: '+DataDirectory)
bins = pd.read_csv(DataDirectory+'/flat/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('loaded the particle file')
n_bins = max(bins['bn'])+1
print('The number of bins is:'+str(n_bins))
fig,(ax) = plt.subplots(figsize=(10,10))
#temp_bins=bins[bins['bn'] == 0]
#print(temp_bins['time'][3])
max_conc = (bins['be_conc']).max()
print('The max Be concentration is: ')
print(max_conc)
colors = plt.cm.viridis(np.linspace(0,1,n_bins))
depth_bins =[[0,0.1],[0.1,0.2],[0.2,0.3],[0.3,0.4],[0.4,0.5],[0.5,0.6],[0.6,0.7],[0.7,0.8],[0.8,0.9],[0.9,1.0]]


ax = plt.subplot(2,2,1)
#Output the Be concentration with depth for each bin and plot but onthe same plot coloured by bin
for i in range(n_bins):
    temp_bins=bins[bins['bn'] == i]
    cb = ax.scatter(temp_bins["be_conc"], temp_bins["d_loc"],s=0.1,c=colors[i], lw = 0, alpha=0.55)
    cb.set_clim(vmin=0,vmax=n_bins-1)
    for j in range(0,len(depth_bins)-1):
        temp = temp_bins[(temp_bins.d_loc >= depth_bins[j][0]) & (temp_bins.d_loc <= depth_bins[j][1])]
        #Find the mean values of each bi
        mean_d = temp.mean().d_loc

        mean_be = temp.mean().be_conc
        be_std = temp.std().be_conc
        d_std = temp.std().d_loc

        ax.scatter(mean_be,mean_d,s=20,color=colors[i])

# Plot the analytical solution?
#Time (a)
t = 10000
#Production rate at surface (atoms/g/a) (taken from Table 6)
p_0 = 2.41 #from LSD mixing model
#Depth of profile (cm)
d = 100
#Depth profile for testing
z = np.arange(0,d,0.1)
#density of material (g/cm^3)
rho = 2.0
#density of quartz (g/cm^3)
rho_q =2.65
e = 0
#Decay Constant
gamma = 0
#attenuation lenth (g/cm^2)
l = 160 #from the LSD mixing model
#Production rate at different depth each year
p_z = p_0*np.exp(-rho*z/l)
#Production for x number of years
p_z_t = p_z*t
ax.plot(p_z_t,z/100,label = 'Lal and Chen Analytical Model',c='k',linestyle='dashed')
ax.set_xlim(0,max_conc)
ax.set_ylim(0,1.0)
plt.gca().invert_yaxis()
ax.legend(loc='upper left',fontsize = 12)
ax.title.set_text('Flat')
# Do the shallow slope
bins = pd.read_csv(DataDirectory+'shallow/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
ax = plt.subplot(2,2,2)
#Output the Be concentration with depth for each bin and plot but onthe same plot coloured by bin
for i in range(n_bins):
    temp_bins=bins[bins['bn'] == i]
    cb = ax.scatter(temp_bins["be_conc"], temp_bins["d_loc"],s=0.1,c=colors[i], lw = 0, alpha=0.55)
    cb.set_clim(vmin=0,vmax=n_bins-1)
    for j in range(0,len(depth_bins)-1):
        temp = temp_bins[(temp_bins.d_loc >= depth_bins[j][0]) & (temp_bins.d_loc <= depth_bins[j][1])]
        #Find the mean values of each bi
        mean_d = temp.mean().d_loc

        mean_be = temp.mean().be_conc
        be_std = temp.std().be_conc
        d_std = temp.std().d_loc

        ax.scatter(mean_be,mean_d,s=20,color=colors[i])

ax.plot(p_z_t,z/100,label = 'Lal and Chen Analytical Model',c='k',linestyle='dashed')
ax.set_xlim(0,max_conc)
ax.set_ylim(0,1.0)
plt.gca().invert_yaxis()
axcb = plt.colorbar(cb)
axcb.ax.set_ylabel('Downslope Bin',fontsize=12)
ax.title.set_text('Shallow')

# Do the moderate slope
bins = pd.read_csv(DataDirectory+'moderate/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
ax = plt.subplot(2,2,3)
#Output the Be concentration with depth for each bin and plot but onthe same plot coloured by bin
for i in range(n_bins):
    temp_bins=bins[bins['bn'] == i]
    cb = ax.scatter(temp_bins["be_conc"], temp_bins["d_loc"],s=0.1,c=colors[i], lw = 0, alpha=0.55)
    cb.set_clim(vmin=0,vmax=n_bins-1)
    for j in range(0,len(depth_bins)-1):
        temp = temp_bins[(temp_bins.d_loc >= depth_bins[j][0]) & (temp_bins.d_loc <= depth_bins[j][1])]
        #Find the mean values of each bi
        mean_d = temp.mean().d_loc

        mean_be = temp.mean().be_conc
        be_std = temp.std().be_conc
        d_std = temp.std().d_loc

        ax.scatter(mean_be,mean_d,s=20,color=colors[i])

ax.plot(p_z_t,z/100,label = 'Lal and Chen Analytical Model',c='k',linestyle='dashed')
ax.set_xlim(0,max_conc)
ax.set_ylim(0,1.0)
plt.gca().invert_yaxis()
ax.title.set_text('Moderate')



# Do the steep slope
bins = pd.read_csv(DataDirectory+'steep/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
ax = plt.subplot(2,2,4)
#Output the Be concentration with depth for each bin and plot but onthe same plot coloured by bin
for i in range(n_bins):
    temp_bins=bins[bins['bn'] == i]
    cb = ax.scatter(temp_bins["be_conc"], temp_bins["d_loc"],s=0.1,c=colors[i], lw = 0, alpha=0.55)
    cb.set_clim(vmin=0,vmax=n_bins-1)
    for j in range(0,len(depth_bins)-1):
        temp = temp_bins[(temp_bins.d_loc >= depth_bins[j][0]) & (temp_bins.d_loc <= depth_bins[j][1])]
        #Find the mean values of each bi
        mean_d = temp.mean().d_loc

        mean_be = temp.mean().be_conc
        be_std = temp.std().be_conc
        d_std = temp.std().d_loc

        ax.scatter(mean_be,mean_d,s=20,color=colors[i])

ax.plot(p_z_t,z/100,label = 'Lal and Chen Analytical Model',c='k',linestyle='dashed')
ax.set_xlim(0,max_conc)
ax.set_ylim(0,1.0)
plt.gca().invert_yaxis()
axcb = plt.colorbar(cb)
axcb.ax.set_ylabel('Downslope Bin',fontsize=12)
ax.title.set_text('Steep')
ax =fig.add_subplot(1,1,1,frameon=False)
ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)







ax.set_ylabel('Depth (m)',fontsize=20)
ax.set_xlabel('$^1$$^0$Be Concentration',fontsize=20)
plt.tight_layout()
plt.savefig(DataDirectory+'hillslope_crn_conc_bins_depth_profile_binned', dpi=100, bbox_inches='tight')



