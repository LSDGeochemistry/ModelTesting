#Script for plotting various hillslope stats by bin from the model output
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from matplotlib.ticker import FormatStrFormatter


DataDirectory = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/idealised_catena_runs/no_mixing_erosion/'

bins = pd.read_csv(DataDirectory+'flat/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )

n_bins = max(bins['bn'])+1
print('The number of bins is:'+str(n_bins))
max_depth=1.0

fig = plt.figure(figsize=(14,14))
for i in range(n_bins):
    temp_bins=bins[(bins['bn'] == i) & (bins['d_loc'] <= max_depth) & (bins['page'] >= 0)]
    ax = fig.add_subplot(6,3,i+1)
    plt.hist(temp_bins['page'],bins=10)
    # print(temp_bins['be_conc'].min())
    ax.annotate('Number of particles: ' + str(len(temp_bins['be_conc'])),xy=(0.95,0.95), xycoords='axes fraction', color='k', fontsize=8, bbox=dict(facecolor='white',edgecolor='white',boxstyle='square, pad=0.3'),ha='right',va='top')


plt.savefig(DataDirectory+'hillslope_crn_conc_bins_hist_flat', dpi=100, bbox_inches='tight')

bins = pd.read_csv(DataDirectory+'shallow/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )

fig = plt.figure(figsize=(14,14))
for i in range(n_bins):
    temp_bins=bins[(bins['bn'] == i) & (bins['d_loc'] <= max_depth) & (bins['page'] >= 0)]
    ax = fig.add_subplot(6,3,i+1)
    plt.hist(temp_bins['page'],bins=10)
    # print(temp_bins['be_conc'].min())
    ax.annotate('Number of particles: ' + str(len(temp_bins['be_conc'])),xy=(0.95,0.95), xycoords='axes fraction', color='k', fontsize=8, bbox=dict(facecolor='white',edgecolor='white',boxstyle='square, pad=0.3'),ha='right',va='top')


plt.savefig(DataDirectory+'hillslope_crn_conc_bins_hist_shallow', dpi=100, bbox_inches='tight')



bins = pd.read_csv(DataDirectory+'moderate/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


fig = plt.figure(figsize=(14,14))
for i in range(n_bins):
    temp_bins=bins[(bins['bn'] == i) & (bins['d_loc'] <= max_depth) & (bins['page'] >= 0)]
    ax = fig.add_subplot(6,3,i+1)
    plt.hist(temp_bins['page'],bins=10)
    # print(temp_bins['be_conc'].min())
    ax.annotate('Number of particles: ' + str(len(temp_bins['be_conc'])),xy=(0.95,0.95), xycoords='axes fraction', color='k', fontsize=8, bbox=dict(facecolor='white',edgecolor='white',boxstyle='square, pad=0.3'),ha='right',va='top')


plt.savefig(DataDirectory+'hillslope_crn_conc_bins_hist_moderate', dpi=100, bbox_inches='tight')


bins = pd.read_csv(DataDirectory+'steep/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )


fig = plt.figure(figsize=(14,14))
for i in range(n_bins):
    temp_bins=bins[(bins['bn'] == i) & (bins['d_loc'] <= max_depth) & (bins['page'] >= 0)]
    ax = fig.add_subplot(6,3,i+1)
    plt.hist(temp_bins['page'],bins=10)
    # print(temp_bins['be_conc'].min())
    ax.annotate('Number of particles: ' + str(len(temp_bins['be_conc'])),xy=(0.95,0.95), xycoords='axes fraction', color='k', fontsize=8, bbox=dict(facecolor='white',edgecolor='white',boxstyle='square, pad=0.3'),ha='right',va='top')


plt.savefig(DataDirectory+'hillslope_crn_conc_bins_hist_steep', dpi=100, bbox_inches='tight')