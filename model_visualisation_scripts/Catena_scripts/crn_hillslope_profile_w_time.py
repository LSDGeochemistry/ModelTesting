#Script for plotting and comparing down  ahillsope transect
from unittest.mock import AsyncMockMixin
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
import warnings
warnings.filterwarnings('ignore')

###User defined parameter for plotting
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/no_mixing/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/hillslope_flux_test/no_mixing_erosion_0_00001/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001/'
# DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001_erosion_0_001/'
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/steady_state_tests/analytical_nonlinear_test/'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/0_1mm_linear/10mm_mixing/'

print('This is the input file directory: '+DataDirectory)
bins = pd.read_csv(DataDirectory+'p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('loaded the particle file')

# load and find the max ds distance from ft file

time_unique = bins.time.unique()
time_unique = np.array(time_unique)
time_unique = time_unique/1000
bins_unique = bins.bn.unique()
bins_unique = np.array(bins_unique)
bins['time'] = bins['time']/1000


# Load the flowtube data
# Set up the ds distance
ft_out = pd.read_csv(DataDirectory+'/ft_properties.out', sep=" ",header=0,names=['s', 'b', 'A', 'zeta', 'eta', 'h'] )
ft_pits = ft_out.s.unique()
ft_pits = np.array(ft_pits)
ft_pits = np.delete(ft_pits, np.where(ft_pits == '-99'))
ft_pits = np.delete(ft_pits, np.where(ft_pits == 's'))
ft_pits = ft_pits.astype(np.float)
div = max(bins_unique)/max(ft_pits)




# Plot the colorbar
colors = plt.cm.viridis(np.linspace(0,1,len(time_unique)))


ax = plt.subplot(1,1,1)


# print(len(plot_bins))
for i in range(0,len(time_unique)):
    print(time_unique[i])
    for j in range(0,len(bins_unique)):
        
        temp_bins = bins[(bins['time'] == time_unique[i]) & (bins['bn'] == bins_unique[j]) & (bins['d_loc'] <= 0.6)]

        mean_crn = temp_bins.mean().be_conc
        
        
        cb = ax.scatter((bins_unique[j]/div),mean_crn,color=colors[i],s=10)
        cb.set_clim(vmin=0,vmax=max(time_unique))
        
    # print(time_unique[i])

# ax.set_ylim(0,30000)
ax.set_xlim(0,max(bins_unique)/div)

axcb = plt.colorbar(cb)
axcb.ax.set_ylabel('Time (kiloyears)',fontsize=12)




ax.set_ylabel(' Mean $^1$$^0$Be Concentration in Soil (atoms g$^-$$^1$)',fontsize=15)
ax.set_xlabel('Distance Downslope (m)',fontsize=20)


plt.tight_layout()
plt.savefig(DataDirectory+'crn_hillsope_profile_with_time_whole_soil_column', dpi=100, bbox_inches='tight')



