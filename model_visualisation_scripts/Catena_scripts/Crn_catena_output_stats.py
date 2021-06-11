#Script for plotting various hillslope stats by bin from the model output
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from matplotlib.ticker import FormatStrFormatter

###User defined parameter for plotting
#Number of profiles (bins)
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001/'
# DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/mixing_0_0001_erosion_0_001/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/steep_slope/no_mixing/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/flux_tests/no_mixing_erosion_0_001/'
#DataDirectory =  'C:/Workspace/github/LSDMixingModel/Runs/hillslope_flux_test/no_mixing_erosion_0_00001/'
# DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/catenas_no_mixing/steep/'
DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/idealised_catena_runs/heavy_mixing/steep/'
#Number of profiles (bins), should rip this straight from model output for simplicity!!!

# n_bins = 10
print('This is the input file directory: '+DataDirectory)
bins = pd.read_csv(DataDirectory+'p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
print('loaded the particle file')
n_bins = max(bins['bn'])+1
print('The number of bins is:'+str(n_bins))
max_depth=1.0
#PLot the age distribution of Be concentration as a function of age in each bin
fig = plt.figure(figsize=(14,14))
for i in range(n_bins):
    temp_bins=bins[(bins['bn'] == i) & (bins['d_loc'] <= max_depth)]
    ax = fig.add_subplot(6,3,i+1)
    cb = ax.scatter(temp_bins["be_conc"], temp_bins["page"],s=0.2,c=temp_bins['bn'],cmap=plt.cm.viridis, label = 'Downslope Bin', lw = 0, alpha=0.25)
    cb.set_clim(vmin=0,vmax=n_bins-1)

plt.savefig(DataDirectory+'hillslope_crn_conc_bins_age', dpi=100, bbox_inches='tight')
#PLot the age distribution of Be concentration in each bin as a histogram
fig = plt.figure(figsize=(14,14))
for i in range(n_bins):
    temp_bins=bins[(bins['bn'] == i) & (bins['d_loc'] <= max_depth)]
    ax = fig.add_subplot(6,3,i+1)
    plt.hist(temp_bins['page'],bins=10)
    # print(temp_bins['be_conc'].min())
    ax.annotate('Number of particles: ' + str(len(temp_bins['be_conc'])),xy=(0.95,0.95), xycoords='axes fraction', color='k', fontsize=8, bbox=dict(facecolor='white',edgecolor='white',boxstyle='square, pad=0.3'),ha='right',va='top')


plt.savefig(DataDirectory+'hillslope_crn_conc_bins_hist', dpi=100, bbox_inches='tight')
#Plot some boxplots to show the range of ages in each bin
plot_bins = [[] for i in range(n_bins)]
print(len(plot_bins))
for i in range(n_bins):
    temp_bins=bins[(bins['bn'] == i) & (bins['d_loc'] <= max_depth)]
    plot_bins[i] = np.append(plot_bins[i], [temp_bins['page']])

fig = plt.figure()
print(len(plot_bins))
ax = fig.add_subplot(1,1,1)
ax.boxplot(plot_bins)
plt.savefig(DataDirectory+'hillslope_crn_conc_bins_box', dpi=100, bbox_inches='tight')


