import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
import os as os
from scipy.interpolate import make_interp_spline, BSpline
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')

fig = plt.figure(figsize=(15,15))

#Set the root directory
root = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/pinedale_17/'
#set number of runs
runs = (len(next(os.walk(root))[1]))
print(runs)
counter = 0
#Create bins, to do this need to set depth first
d =1.5
bins = [[0.01, 0.05], [0.05, 0.15], [0.1, 0.3], [0.2, 0.4], [0.48, 0.68], [0.78, 0.98], [1.23, 1.43]]
#set figure size

ax=fig.add_subplot(2,3,1)

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
    for j in range(0,len(bins)-1):
        groups = data[(data.d_loc >= bins[j][0]) & (data.d_loc <= bins[j][1])]
        #Find the mean values of each bin
        mean_d = groups.mean().d_loc
        mean_be = groups.mean().be_conc
        be_std = groups.std().be_conc
        d_std = groups.std().d_loc
        rate_key = (mix_rates[i]*1000)
        rate_key= str(rate_key)






        #Set the colourmap to colour by run number which corresponds to varying mixing velocity
        # cm = np.full(len(mean_be),counter)
        cb = ax.scatter(mean_be,mean_d,s=20,c=colors[counter],label=rate_key if j == 0 else '')
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
ax.set_title('Pinedale (17 kyr)',fontsize=12)
ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
#plt.plot(be_conc,d_loc,linewidth=1,c='k')
ax.legend(title='Mixing rate (mm a$^-1$)',loc=4)
ax.set_ylim(0,d)
plt.gca().invert_yaxis()


#Set the root directory
root = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/pinedale_19/'
#set number of runs
runs = (len(next(os.walk(root))[1]))

counter = 0
#Create bins, to do this need to set depth first
d =1.5
bins = [[0.01, 0.05], [0.05, 0.15], [0.1, 0.3], [0.2, 0.4], [0.48, 0.68], [0.78, 0.98], [1.23, 1.43]]
#set figure size

ax=fig.add_subplot(2,3,2)

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
    for j in range(0,len(bins)-1):
        groups = data[(data.d_loc >= bins[j][0]) & (data.d_loc <= bins[j][1])]
        #Find the mean values of each bin
        mean_d = groups.mean().d_loc
        mean_be = groups.mean().be_conc
        be_std = groups.std().be_conc
        d_std = groups.std().d_loc
        rate_key = (mix_rates[i]*1000)
        rate_key= str(rate_key)






        #Set the colourmap to colour by run number which corresponds to varying mixing velocity
        # cm = np.full(len(mean_be),counter)
        cb = ax.scatter(mean_be,mean_d,s=20,c=colors[counter],label=rate_key if j == 0 else '')
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
ax.set_title('Pinedale (19 kyr)',fontsize=12)
#plt.plot(be_conc,d_loc,linewidth=1,c='k')
ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax.legend(title='Mixing rate (mm a$^-1$)',loc=4)
ax.set_ylim(0,d)
plt.gca().invert_yaxis()


#Set the root directory
root = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/pinedale_21/'
#set number of runs
runs = (len(next(os.walk(root))[1]))
print(runs)
counter = 0
#Create bins, to do this need to set depth first
bins = [[0.01, 0.05], [0.05, 0.15], [0.1, 0.3], [0.2, 0.4], [0.48, 0.68], [0.78, 0.98], [1.23, 1.43]]

#set figure size

ax=fig.add_subplot(2,3,3)

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
    for j in range(0,len(bins)-1):
        groups = data[(data.d_loc >= bins[j][0]) & (data.d_loc <= bins[j][1])]
        #Find the mean values of each bin
        mean_d = groups.mean().d_loc
        mean_be = groups.mean().be_conc
        be_std = groups.std().be_conc
        d_std = groups.std().d_loc
        rate_key = (mix_rates[i]*1000)
        rate_key= str(rate_key)






        #Set the colourmap to colour by run number which corresponds to varying mixing velocity
        # cm = np.full(len(mean_be),counter)
        cb = ax.scatter(mean_be,mean_d,s=20,c=colors[counter],label=rate_key if j == 0 else '')
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
ax.set_title('Pinedale (21 kyr)',fontsize=12)
#plt.plot(be_conc,d_loc,linewidth=1,c='k')
ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax.legend(title='Mixing rate (mm a$^-1$)',loc=4)
ax.set_ylim(0,d)
plt.gca().invert_yaxis()
# axcb = plt.colorbar(cb)
# plt.show()


#Set the root directory
root = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/bull_lake_65/'
#set number of runs
runs = (len(next(os.walk(root))[1]))
print(runs)
counter = 0

initial_data = pd.read_csv('/exports/csce/datastore/geos/users/s0933963/github/ModelTesting/master_param/bull_lake/bull_lake.csv', sep=",",skiprows=[0], names =['upp_d','low_d','be_conc','depth','d_err','be_err'])

bins = [[0.03, 0.07], [0.15, 0.25], [0.23, 0.33], [0.38, 0.48], [0.59, 0.69], [0.69, 0.89], [0.94, 1.14], [1.2, 1.4]]

d_err = initial_data['d_err'].values

d= 1.50

#set figure size
ax=fig.add_subplot(2,3,4)
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
ax.set_title('Bull Lake 65 (kyr)',fontsize=12)
ax.scatter(be_conc,d_loc,s=20,c='k',label='Bull Run data')
ax.errorbar(be_conc,d_loc,xerr=be_err,yerr=d_err, fmt='none',c='k',ls='--')
ax.legend(title='Mixing rate (mm a$^-1$)',loc=4)
ax.set_ylim(0,d)
plt.gca().invert_yaxis()

#Set the root directory
root = '/exports/csce/datastore/geos/users/s0933963/github/LSDMixingModel/Runs/bull_lake_67/'
#set number of runs
runs = (len(next(os.walk(root))[1]))
print(runs)
counter = 0

initial_data = pd.read_csv('/exports/csce/datastore/geos/users/s0933963/github/ModelTesting/master_param/bull_lake/bull_lake.csv', sep=",",skiprows=[0], names =['upp_d','low_d','be_conc','depth','d_err','be_err'])

bins = [[0.03, 0.07], [0.15, 0.25], [0.23, 0.33], [0.38, 0.48], [0.59, 0.69], [0.69, 0.89], [0.94, 1.14], [1.2, 1.4]]

d_err = initial_data['d_err'].values

d= 1.50

#set figure size
ax=fig.add_subplot(2,3,5)
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
ax.set_title('Bull Lake (67.5 kyr)',fontsize=12)
ax.scatter(be_conc,d_loc,s=20,c='k',label='Bull Run data')
ax.errorbar(be_conc,d_loc,xerr=be_err,yerr=d_err, fmt='none',c='k',ls='--')
ax.legend(title='Mixing rate (mm a$^-1$)',loc=4)
ax.set_ylim(0,d)
plt.gca().invert_yaxis()

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
ax=fig.add_subplot(2,3,6)
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
ax.set_title('Bull Lake (72 kyr)',fontsize=12)
ax.scatter(be_conc,d_loc,s=20,c='k',label='Bull Run data')
ax.errorbar(be_conc,d_loc,xerr=be_err,yerr=d_err, fmt='none',c='k',ls='--')
ax.legend(title='Mixing rate (mm a$^-1$)',loc=4)
ax.set_ylim(0,d)
plt.gca().invert_yaxis()




ax =fig.add_subplot(1,1,1,frameon=False)
ax.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
ax.set_ylabel('Depth (m)',fontsize=18)

ax.set_xlabel('$^1$$^0$Be Concentration atoms g$^-$$^1$',fontsize=16)
ax.xaxis.labelpad = 14
plt.savefig(root+'be_conc_depth_changing_mixing.png', dpi=100, bbox_inches='tight')