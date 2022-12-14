#Script for plotting and comparing down  ahillsope transect
import warnings
warnings.filterwarnings('ignore')
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
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/0_1mm/0mm_mixing/'
#Number of profiles (bins), should rip this straight from model output for simplicity!!!
# Do the flat section
print('This is the input file directory: '+DataDirectory)
bins = pd.read_csv(DataDirectory+'p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('loaded the particle file')
n_bins = max(bins['bn'])+1
print('The number of bins is:'+str(n_bins))
# fig,(ax) = plt.subplots(figsize=(40,10))
#temp_bins=bins[bins['bn'] == 0]
#print(temp_bins['time'][3])
fig=plt.figure()
n_time = bins.time.unique()
print(len(n_time))

colors = plt.cm.viridis(np.linspace(0,1,n_bins))
depth_bins =[[0,0.1],[0.1,0.2],[0.2,0.3],[0.3,0.4],[0.4,0.5],[0.5,0.6],[0.6,0.7],[0.7,0.8],[0.8,0.9],[0.9,1.0]]



#Output the Be concentration with depth for each bin and plot but onthe same plot coloured by bin
for time in range(0,len(n_time)):
    age_bins = bins[(bins.time == n_time[time])]
    ax= fig.add_subplot(1,5,time+1)
    for i in range(n_bins):
        max_age = []
        temp_bins=age_bins[age_bins['bn'] == i]
        cb = ax.scatter(temp_bins["be_conc"], temp_bins["d_loc"],s=0.1,c=colors[i], lw = 0, alpha=0.55)
        cb.set_clim(vmin=0,vmax=n_bins-1)
        for j in range(0,len(depth_bins)-1):
            temp = temp_bins[(temp_bins.d_loc >= depth_bins[j][0]) & (temp_bins.d_loc <= depth_bins[j][1])]
            #Find the mean values of each bin
            mean_d = temp.mean().d_loc

            mean_be = temp.mean().be_conc
            be_std = temp.std().be_conc
            d_std = temp.std().d_loc
            temp_max_age = temp.max().be_conc

            max_age.append(temp_max_age)
            ax.scatter(mean_be,mean_d,s=20,color=colors[i])


        ax.set_ylim(0,0.8)
        ax.set_xlim(0,max(max_age))
        plt.gca().invert_yaxis()
axcb = plt.colorbar(cb)
            # axcb.ax.set_ylabel('Downslope Bin',fontsize=12)
            #
            # ax.set_ylabel('Depth (m)',fontsize=20)
            # ax.set_xlabel('$^1$$^0$Be Concentration',fontsize=20)

plt.tight_layout()
plt.savefig(DataDirectory+'hillslope_crn_conc_bins_depth_profile_binned_with_time', dpi=100, bbox_inches='tight')



