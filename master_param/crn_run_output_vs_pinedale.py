import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
import os as os
from scipy.interpolate import make_interp_spline, BSpline
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')
#Set the root directory
root = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/pinedale_17/'
#set number of runs
runs = (len(next(os.walk(root))[1]))
print(runs)
counter = 0
#Create bins, to do this need to set depth first
d =1.5
bins = np.linspace(0,d,30)
#set figure size
fig = plt.figure(figsize=(10,10))
ax=fig.add_subplot(1,1,1)

mix_rates=[]
#Now set up the list of file names for plotting
for subdirs, dirs, files in os.walk(root):
    for dirs in dirs:
        temp = dirs[16:]
        temp = temp.replace('_','.')
        rate = float(temp)
        mix_rates.append(rate)
        dir = dirs[:16]
mix_rates.sort()

for i in range(0,len(mix_rates)):
    mix_rate = str(mix_rates[i])
    mix_rate = mix_rate.replace('.','_')
    mix_rate = str(mix_rate)
    colors = plt.cm.viridis(np.linspace(0,1,runs))
    data = pd.read_csv(root+dir+mix_rate+'/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
    print('loaded '+str(dir)+mix_rate)
    data = data.drop(data[data.d_loc >= d].index)
        #Bin the data into a number of bins set above
    groups = data.groupby(np.digitize(data.d_loc,bins))
        #Find the mean values of each bin
    mean_d = groups.mean().d_loc.values
    mean_be = groups.mean().be_conc.values
    be_std = groups.std().be_conc.values
    d_std = groups.std().d_loc.values
    rate_key = (mix_rates[i]*1000)
    rate_key= str(rate_key)






    #Set the colourmap to colour by run number which corresponds to varying mixing velocity
    # cm = np.full(len(mean_be),counter)
    cb = ax.scatter(mean_be,mean_d,s=20,c=colors[counter],label=rate_key)
    # ax.errorbar(mean_be,mean_d,xerr=be_std,yerr=d_std, fmt='none')
    cb.set_clim(vmin=0,vmax=runs)
    counter+= 1

#Now load the initial data to test the model against
initial_data = pd.read_csv('/exports/csce/datastore/geos/users/s0933963/github/ModelTesting/master_param/pinedale/pinedale.csv', sep=",",skiprows=[0], names =['upp_d','low_d','be_conc','depth','d_err','be_err'])
#print(initial_data)
be_conc = initial_data['be_conc'].values
#Convert the values to be the same as the outputted data
be_conc = be_conc*100000
#print(be_conc)
d_loc = initial_data['depth'].values
#print(d_loc)
#Get the error bars
be_err = initial_data['be_err'].values
be_err = be_err*100000
d_err = initial_data['d_err'].values
ax.scatter(be_conc,d_loc,s=20,c='k',marker='x')
ax.errorbar(be_conc,d_loc,xerr=be_err,yerr=d_err, fmt='none',c='k')

#plt.plot(be_conc,d_loc,linewidth=1,c='k')
ax.legend()
ax.set_ylim(0,d)
plt.gca().invert_yaxis()
# axcb = plt.colorbar(cb)
# plt.show()
plt.savefig(root+'be_conc_depth_changing_mixing', dpi=100, bbox_inches='tight')