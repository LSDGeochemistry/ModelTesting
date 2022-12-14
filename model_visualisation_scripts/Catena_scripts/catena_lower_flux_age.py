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
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/0_1mm_linear/0mm_mixing/'
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/changing_base_level/0_1mm/1mm_mixing/'
#Number of profiles (bins), should rip this straight from model output for simplicity!!!
# Do the flat section
print('This is the input file directory: '+DataDirectory)
bins = pd.read_csv(DataDirectory+'ep_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('loaded the particle file')


time_unique = bins.time.unique()
time_unique = np.array(time_unique)
timelabels = time_unique/1000


# print(timelabels)
# print(len(time_unique))
plot_bins = [[] for i in (time_unique)]
# print(len(plot_bins))
for i in range(0,len(time_unique)):
    temp_bins=bins[(bins['time'] == time_unique[i]) & (bins['bn'] == bins.bn.max())]
    # print(time_unique[i])
    plot_bins[i] = np.append(plot_bins[i], [temp_bins['page']])


ax = plt.subplot(1,1,1)

# print(len(plot_bins))
# print(len(timelabels))

ax.violinplot(plot_bins,showextrema=False,showmedians=True,showmeans=True)
# ax.set_ylim(0,400000)
ax.set_ylabel('Particle Age',fontsize=20)
ax.set_xlabel('Time (kiloyears)',fontsize=20)


plt.tight_layout()
plt.savefig(DataDirectory+'hillslope_crn_conc_flux_output_age', dpi=100, bbox_inches='tight')



