import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
import os as os
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')

#Set the root directory
root = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/bull_lake_72/'
#set number of runs
runs = (len(next(os.walk(root))[1]))
print(runs)
counter = 0

initial_data = pd.read_csv('/exports/csce/datastore/geos/users/s0933963/github/ModelTesting/master_param/bull_lake/bull_lake.csv', sep=",",skiprows=[0], names =['upp_d','low_d','be_conc','depth','d_err','be_err'])

bins = [[0.03, 0.07], [0.15, 0.25], [0.23, 0.33], [0.38, 0.48], [0.59, 0.69], [0.69, 0.89], [0.94, 1.14], [1.2, 1.4]]

d_err = initial_data['d_err'].values

d= 1.50

#set figure size
fig = plt.figure(figsize=(10,10))
ax=fig.add_subplot(1,1,1)
mix_rates=[]
#Now set up the list of file names for plotting
for subdirs, dirs, files in os.walk(root):
    for dirs in dirs:
        temp = dirs[17:]
        temp = temp.replace('_','.')
        rate = float(temp)
        mix_rates.append(rate)
        dir = dirs[:17]
mix_rates.sort()





for i in range(0,len(mix_rates)):
        mix_rate = str(mix_rates[i])
        mix_rate = mix_rate.replace('.','_')
        mix_rate = str(mix_rate)

        data = pd.read_csv(root+dir+mix_rate+'/p_trans_out.pout', sep=" ",names=['time', 'bn', 'pid','z_loc','s_loc','d_loc','buff','page','osl','be_conc','fallout_be_conc','c_conc','ne_conc'] )
        print('loaded '+str(dir)+mix_rate)
        colors = plt.cm.viridis(np.linspace(0,1,runs))
        #Bin the data into a number of bins set above
        for j in range(0,len(bins)-1):
            temp = data[(data.d_loc >= bins[j][0]) & (data.d_loc <= bins[j][1])]

        #Find the mean values of each bi
            mean_d = temp.mean().d_loc

            mean_be = temp.mean().be_conc
            be_std = temp.std().be_conc
            d_std = temp.std().d_loc
            rate_key = (mix_rates[i]*1000)
            rate_key= str(rate_key)

            cb = ax.scatter(mean_be,mean_d,s=20,color=colors[counter], label=rate_key if j == 0 else '')

            # ax.errorbar(mean_be,mean_d,xerr=be_std,yerr=d_std, fmt='none',color='k')
            cb.set_clim(vmin=0,vmax=runs)

        #print(counter)
        counter+= 1

#Now load the initial data to test the model against

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

ax.scatter(be_conc,d_loc,s=20,c='k',label='Bull Run data')
ax.errorbar(be_conc,d_loc,xerr=be_err,yerr=d_err, fmt='none',c='k',ls='--')
ax.legend()
ax.set_ylim(0,d)
plt.gca().invert_yaxis()
# axcb = plt.colorbar(cb)
# plt.show()
plt.savefig(root+'be_conc_depth_changing_mixing', dpi=100, bbox_inches='tight')